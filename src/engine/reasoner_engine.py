import json
import multiprocessing
import tempfile
import time
from enum import Enum
from pathlib import Path
from typing import Any

from rdflib import Graph

from src.core.config import settings


class ReasonerType(str, Enum):
    HERMIT = "hermit"
    PELLET = "pellet"


def _reasoner_worker(rdfxml_path: str, reasoner_type: str, result_file: str):
    """Worker function that runs in a subprocess. Writes JSON result to file."""
    import gc
    import time

    start = time.time()
    try:
        from owlready2 import World, sync_reasoner_hermit, sync_reasoner_pellet
        from owlready2 import OwlReadyInconsistentOntologyError

        world = World()
        try:
            onto = world.get_ontology(f"file://{rdfxml_path}").load()

            try:
                if reasoner_type == "hermit":
                    sync_reasoner_hermit(onto, infer_property_values=True, debug=0)
                else:
                    sync_reasoner_pellet(onto, infer_property_values=True, debug=0)
                inconsistent = [str(c) for c in onto.inconsistent_classes()]
            except OwlReadyInconsistentOntologyError:
                # A globally inconsistent ontology surfaces as this exception, not
                # via inconsistent_classes(). This is a valid result, not an error.
                inconsistent = []
                result = {
                    "reasoner": reasoner_type,
                    "is_consistent": False,
                    "inconsistent_classes": [],
                    "execution_time_seconds": round(time.time() - start, 3),
                    "error": None,
                }
                Path(result_file).write_text(json.dumps(result))
                return

            result = {
                "reasoner": reasoner_type,
                "is_consistent": len(inconsistent) == 0,
                "inconsistent_classes": inconsistent,
                "execution_time_seconds": round(time.time() - start, 3),
                "error": None,
            }
        finally:
            try:
                world.close()
            except Exception:
                pass
            gc.collect()

    except Exception as e:
        result = {
            "reasoner": reasoner_type,
            "is_consistent": False,
            "inconsistent_classes": [],
            "execution_time_seconds": round(time.time() - start, 3),
            "error": str(e),
        }

    Path(result_file).write_text(json.dumps(result))


def run_reasoner(
    rdfxml_path: str,
    reasoner_type: ReasonerType,
    timeout: int | None = None,
) -> dict[str, Any]:
    """Run a reasoner in an isolated subprocess with timeout."""
    timeout = timeout or settings.reasoner_timeout

    if not Path(rdfxml_path).exists():
        return {
            "reasoner": reasoner_type.value,
            "is_consistent": False,
            "inconsistent_classes": [],
            "execution_time_seconds": 0.0,
            "error": f"RDF/XML file not found: {rdfxml_path}",
        }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        result_file = f.name

    ctx = multiprocessing.get_context("spawn")
    proc = ctx.Process(
        target=_reasoner_worker,
        args=(rdfxml_path, reasoner_type.value, result_file),
    )
    start = time.time()
    proc.start()
    proc.join(timeout=timeout)

    if proc.is_alive():
        proc.kill()
        proc.join()
        return {
            "reasoner": reasoner_type.value,
            "is_consistent": False,
            "inconsistent_classes": [],
            "execution_time_seconds": round(time.time() - start, 3),
            "error": f"Reasoning timed out after {timeout}s",
        }

    result_path = Path(result_file)
    if result_path.exists():
        try:
            result = json.loads(result_path.read_text())
            return result
        finally:
            result_path.unlink(missing_ok=True)

    return {
        "reasoner": reasoner_type.value,
        "is_consistent": False,
        "inconsistent_classes": [],
        "execution_time_seconds": round(time.time() - start, 3),
        "error": "Subprocess completed but produced no result",
    }


def content_to_rdfxml_file(content: str, format: str = "turtle") -> str:
    """Convert ontology content to a temporary RDF/XML file for reasoners."""
    g = Graph()
    g.parse(data=content, format=format)
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".xml", delete=False)
    g.serialize(destination=tmp.name, format="xml")
    return tmp.name
