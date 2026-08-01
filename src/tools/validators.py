import time
from pathlib import Path
from typing import Literal

from fastmcp import FastMCP

from src.core.file_resolver import resolve_content
from src.core.formatter import format_syntax_result, format_oops_result, format_reasoning_result
from src.engine.syntax_engine import validate_syntax as _validate_syntax
from src.engine.oops_engine import run_oops_scan
from src.engine.reasoner_engine import run_reasoner, content_to_rdfxml_file, ReasonerType

validators_mcp = FastMCP("validators")


@validators_mcp.tool(annotations={"readOnlyHint": True})
def validate_syntax(
    file_path: str | None = None,
    owl_content: str | None = None,
    format: Literal["turtle", "xml", "n3", "nt", "json-ld"] = "turtle",
) -> dict:
    """Validate RDF/OWL syntax using rdflib. Accepts a file path or inline OWL content."""
    start = time.time()
    content = resolve_content(file_path, owl_content)
    data = _validate_syntax(content, format=format)
    elapsed = round(time.time() - start, 3)
    return {
        "success": data["valid"],
        "tool": "validate_syntax",
        "data": data,
        "markdown_summary": format_syntax_result(data),
        "execution_time_seconds": elapsed,
    }


@validators_mcp.tool(annotations={"readOnlyHint": True})
def validate_oops(
    file_path: str | None = None,
    owl_content: str | None = None,
    input_format: Literal["turtle", "xml", "n3", "nt", "json-ld"] = "turtle",
) -> dict:
    """Run OOPs pitfall scanner on an OWL ontology. Detects 22 modeling anti-patterns with severity levels."""
    start = time.time()
    content = resolve_content(file_path, owl_content)
    data = run_oops_scan(content, input_format=input_format)
    elapsed = round(time.time() - start, 3)
    return {
        "success": not data.get("error"),
        "tool": "validate_oops",
        "data": data,
        "markdown_summary": format_oops_result(data),
        "execution_time_seconds": elapsed,
    }


@validators_mcp.tool(annotations={"readOnlyHint": True})
def validate_reasoning(
    file_path: str | None = None,
    owl_content: str | None = None,
    reasoner: Literal["hermit", "pellet", "both"] = "both",
    format: Literal["turtle", "xml", "n3", "nt", "json-ld"] = "turtle",
) -> dict:
    """Check logical consistency using HermiT and/or Pellet OWL reasoners."""
    start = time.time()
    content = resolve_content(file_path, owl_content)
    rdfxml_path = content_to_rdfxml_file(content, format=format)

    try:
        results = []
        if reasoner in ("hermit", "both"):
            results.append(run_reasoner(rdfxml_path, ReasonerType.HERMIT))
        if reasoner in ("pellet", "both"):
            results.append(run_reasoner(rdfxml_path, ReasonerType.PELLET))
    finally:
        Path(rdfxml_path).unlink(missing_ok=True)

    elapsed = round(time.time() - start, 3)
    all_consistent = all(r["is_consistent"] for r in results)
    data = {"results": results, "all_consistent": all_consistent}
    return {
        "success": all_consistent,
        "tool": "validate_reasoning",
        "data": data,
        "markdown_summary": format_reasoning_result(data),
        "execution_time_seconds": elapsed,
    }
