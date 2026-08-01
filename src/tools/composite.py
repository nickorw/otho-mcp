import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Literal

from fastmcp import FastMCP

from src.core.file_resolver import resolve_content, resolve_folder
from src.core.formatter import format_syntax_result, format_oops_result, format_reasoning_result
from src.engine.syntax_engine import validate_syntax as _validate_syntax
from src.engine.oops_engine import run_oops_scan
from src.engine.reasoner_engine import run_reasoner, content_to_rdfxml_file, ReasonerType

composite_mcp = FastMCP("composite")


@composite_mcp.tool(annotations={"readOnlyHint": True})
def validate_all(
    file_path: str | None = None,
    owl_content: str | None = None,
    format: Literal["turtle", "xml", "n3", "nt", "json-ld"] = "turtle",
) -> dict:
    """Run full validation battery: syntax + OOPs pitfalls + reasoning consistency."""
    start = time.time()
    content = resolve_content(file_path, owl_content)

    syntax_data = _validate_syntax(content, format=format)
    oops_data = run_oops_scan(content, input_format=format)

    rdfxml_path = content_to_rdfxml_file(content, format=format)
    try:
        hermit_result = run_reasoner(rdfxml_path, ReasonerType.HERMIT)
        pellet_result = run_reasoner(rdfxml_path, ReasonerType.PELLET)
    finally:
        Path(rdfxml_path).unlink(missing_ok=True)

    reasoning_data = {
        "results": [hermit_result, pellet_result],
        "all_consistent": hermit_result["is_consistent"] and pellet_result["is_consistent"],
    }

    all_pass = syntax_data["valid"] and not oops_data.get("error") and reasoning_data["all_consistent"]
    elapsed = round(time.time() - start, 3)

    md = "\n\n---\n\n".join([
        format_syntax_result(syntax_data),
        format_oops_result(oops_data),
        format_reasoning_result(reasoning_data),
    ])
    return {
        "success": all_pass,
        "tool": "validate_all",
        "data": {"syntax": syntax_data, "oops": oops_data, "reasoning": reasoning_data},
        "markdown_summary": f"# Full Validation Battery\n\n{'✅ All checks passed' if all_pass else '⚠️ Some checks failed'}\n\n{md}",
        "execution_time_seconds": elapsed,
    }


def _process_file(file_path: Path, checks: list, format: str) -> dict:
    """Process a single file for batch validation."""
    file_result = {"file": file_path.name}
    content = file_path.read_text(encoding="utf-8")

    if "syntax" in checks:
        file_result["syntax"] = _validate_syntax(content, format=format)
    if "oops" in checks:
        file_result["oops"] = run_oops_scan(content, input_format=format)
    if "reasoning" in checks:
        rdfxml_path = content_to_rdfxml_file(content, format=format)
        try:
            hermit = run_reasoner(rdfxml_path, ReasonerType.HERMIT)
            file_result["reasoning"] = {"results": [hermit], "all_consistent": hermit["is_consistent"]}
        finally:
            Path(rdfxml_path).unlink(missing_ok=True)

    return file_result


@composite_mcp.tool(annotations={"readOnlyHint": True})
def validate_batch(
    folder_path: str,
    checks: list[Literal["syntax", "oops", "reasoning"]] | None = None,
    pattern: str = "*.owl",
    format: Literal["turtle", "xml", "n3", "nt", "json-ld"] = "turtle",
) -> dict:
    """Run selected validators on all ontology files in a folder."""
    start = time.time()
    checks = checks or ["syntax", "oops", "reasoning"]
    folder = resolve_folder(folder_path)
    files = sorted(folder.glob(pattern))

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(_process_file, f, checks, format) for f in files]
        results = [fut.result() for fut in futures]

    elapsed = round(time.time() - start, 3)
    total = len(results)
    syntax_valid = sum(1 for r in results if r.get("syntax", {}).get("valid", True))

    md_lines = [f"## Batch Validation\n\n**{total} files** processed in {elapsed}s\n"]
    md_lines.append("| File | Syntax | OOPs | Reasoning |")
    md_lines.append("|------|--------|------|-----------|")
    for r in results:
        syn = "✅" if r.get("syntax", {}).get("valid", True) else "❌"
        oops_ok = "✅" if not r.get("oops", {}).get("has_pitfalls", False) else f"⚠️ {r.get('oops', {}).get('pitfall_count', 0)}"
        reas = "✅" if r.get("reasoning", {}).get("all_consistent", True) else "❌"
        md_lines.append(f"| {r['file']} | {syn} | {oops_ok} | {reas} |")

    return {
        "success": syntax_valid == total,
        "tool": "validate_batch",
        "data": {"results": results, "aggregate": {"total": total, "syntax_valid": syntax_valid}},
        "markdown_summary": "\n".join(md_lines),
        "execution_time_seconds": elapsed,
    }


@composite_mcp.tool(annotations={"readOnlyHint": True})
def oops_report(
    folder_path: str,
    pattern: str = "*.owl",
    input_format: Literal["turtle", "xml", "n3", "nt", "json-ld"] = "turtle",
) -> dict:
    """Run OOPs pitfall scanner on all ontologies in a folder and produce a unified severity report."""
    start = time.time()
    folder = resolve_folder(folder_path)
    files = sorted(folder.glob(pattern))

    file_results = []
    summary = {"total": 0, "no_pitfalls": 0, "minor_only": 0, "serious": 0, "failed": 0}

    for f in files:
        summary["total"] += 1
        try:
            content = f.read_text(encoding="utf-8")
            result = run_oops_scan(content, input_format=input_format)
            result["file"] = f.name

            if result.get("error"):
                summary["failed"] += 1
            elif not result["has_pitfalls"]:
                summary["no_pitfalls"] += 1
            else:
                severities = {p["importance"] for p in result["pitfalls"]}
                if severities <= {"Minor"}:
                    summary["minor_only"] += 1
                else:
                    summary["serious"] += 1
            file_results.append(result)
        except Exception as e:
            summary["failed"] += 1
            file_results.append({"file": f.name, "error": str(e), "has_pitfalls": False, "pitfalls": []})

    elapsed = round(time.time() - start, 3)

    md_lines = ["## OOPs Batch Report\n"]
    md_lines.append("| Total | No Pitfalls | Minor Only | Serious | Failed |")
    md_lines.append("|-------|-------------|------------|---------|--------|")
    md_lines.append(f"| {summary['total']} | {summary['no_pitfalls']} | {summary['minor_only']} | {summary['serious']} | {summary['failed']} |")
    md_lines.append("")
    for r in file_results:
        md_lines.append(f"### {r.get('file', 'unknown')}")
        md_lines.append(format_oops_result(r))
        md_lines.append("")

    return {
        "success": True,
        "tool": "oops_report",
        "data": {"summary": summary, "results": file_results},
        "markdown_summary": "\n".join(md_lines),
        "execution_time_seconds": elapsed,
    }
