import json
import time
from pathlib import Path
from typing import Literal

from fastmcp import FastMCP

from src.core.file_resolver import resolve_content
from src.core.formatter import format_metrics_result, format_conversion_result
from src.engine.metrics_engine import compute_metrics
from src.engine.converter_engine import convert_format as _convert

utilities_mcp = FastMCP("utilities")

_CATALOG_PATH = Path(__file__).parent.parent / "data" / "pitfall_catalog.json"
_CATALOG: dict | None = None


def _load_catalog() -> dict:
    global _CATALOG
    if _CATALOG is None:
        _CATALOG = json.loads(_CATALOG_PATH.read_text(encoding="utf-8"))
    return _CATALOG


@utilities_mcp.tool(annotations={"readOnlyHint": True})
def convert_format(
    file_path: str | None = None,
    owl_content: str | None = None,
    source_format: Literal["turtle", "xml", "n3", "nt", "json-ld"] = "turtle",
    target_format: Literal["turtle", "xml", "n3", "nt", "json-ld", "pretty-xml"] = "xml",
) -> dict:
    """Convert ontology between RDF serialization formats (turtle, xml, n3, nt, json-ld)."""
    start = time.time()
    content = resolve_content(file_path, owl_content)
    converted = _convert(content, source_format, target_format)
    elapsed = round(time.time() - start, 3)
    return {
        "success": True,
        "tool": "convert_format",
        "data": {"content": converted, "source_format": source_format, "target_format": target_format},
        "markdown_summary": format_conversion_result(converted, target_format),
        "execution_time_seconds": elapsed,
    }


@utilities_mcp.tool(annotations={"readOnlyHint": True})
def ontology_metrics(
    file_path: str | None = None,
    owl_content: str | None = None,
    format: Literal["turtle", "xml", "n3", "nt", "json-ld"] = "turtle",
) -> dict:
    """Compute comprehensive structural metrics: axiom counts, hierarchy, OntoQA ratios, complexity, lexical quality."""
    start = time.time()
    content = resolve_content(file_path, owl_content)
    data = compute_metrics(content, format=format)
    elapsed = round(time.time() - start, 3)
    return {
        "success": True,
        "tool": "ontology_metrics",
        "data": data,
        "markdown_summary": format_metrics_result(data),
        "execution_time_seconds": elapsed,
    }


@utilities_mcp.tool(annotations={"readOnlyHint": True})
def explain_pitfall(pitfall_code: str) -> dict:
    """Look up a detailed explanation for an OOPs pitfall code (e.g. P08, P11)."""
    catalog = _load_catalog()
    digits = "".join(c for c in pitfall_code if c.isdigit())
    code = f"P{int(digits):02d}" if digits else pitfall_code.upper().strip()

    entry = catalog.get(code)
    if not entry:
        return {
            "success": False,
            "tool": "explain_pitfall",
            "data": {"error": f"Unknown pitfall code: {code}"},
            "markdown_summary": f"❌ Unknown pitfall code: {code}",
            "execution_time_seconds": 0.0,
        }

    md = f"## {entry['code']}: {entry['name']}\n\n"
    md += f"**Severity:** {entry['importance']}\n\n"
    md += f"**Description:** {entry['description']}\n\n"
    md += f"**How to fix:** {entry['how_to_fix']}"

    return {
        "success": True,
        "tool": "explain_pitfall",
        "data": entry,
        "markdown_summary": md,
        "execution_time_seconds": 0.0,
    }
