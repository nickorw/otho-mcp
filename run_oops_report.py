#!/usr/bin/env python3
"""
Runs OOPS! pitfall scanner on all ontologies in data/output/ontologies
and produces a full Markdown report at oops_report.md.
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from src.reviewers.reviewer import OopsPitfallReviewer
from src.utils.oops_parser import parse_oops_response

ONTOLOGIES_DIR = Path("data/output/ontologies")
OUTPUT_REPORT = Path("oops_report.md")
OOPS_ENDPOINT = "http://localhost/OOPS/rest"
ALL_PITFALLS = ["2,3,4,5,6,7,8,10,11,12,13,19,20,21,22,24,25,26,27,28,29"]

IMPORTANCE_ORDER = {"Critical": 0, "Important": 1, "Minor": 2}


def run():
    reviewer = OopsPitfallReviewer(endpoint=OOPS_ENDPOINT)
    owl_files = sorted(ONTOLOGIES_DIR.glob("*.owl"))

    if not owl_files:
        print(f"No .owl files found in {ONTOLOGIES_DIR}")
        sys.exit(1)

    print(f"Found {len(owl_files)} ontologies. Running OOPS...\n")

    passed = []
    failed_analysis = []  # OOPS could not analyse
    with_pitfalls = []

    for owl_file in owl_files:
        print(f"  Analysing {owl_file.name} ...", end=" ", flush=True)
        try:
            raw_xml = reviewer.review_owl_file(str(owl_file), pitfalls=ALL_PITFALLS)

            # Detect OOPS wrong_execution response (different RDF namespace)
            if "wrong_execution" in raw_xml or "oops.linkeddata.es/data/wrong_execution" in raw_xml:
                failed_analysis.append({
                    "file": owl_file.name,
                    "error": "OOPS could not analyse the ontology (wrong_execution response)",
                })
                print("UNABLE TO ANALYSE")
                continue

            result = parse_oops_response(raw_xml)

            if result.get("oops_error"):
                failed_analysis.append({
                    "file": owl_file.name,
                    "error": result.get("error", "Unknown error"),
                })
                print("ERROR (parse)")
            elif not result["has_pitfalls"]:
                passed.append(owl_file.name)
                print("PASSED")
            else:
                with_pitfalls.append({
                    "file": owl_file.name,
                    "pitfalls": result["pitfalls"],
                    "pitfall_count": result["pitfall_count"],
                })
                print(f"PITFALLS ({result['pitfall_count']})")

        except Exception as e:
            failed_analysis.append({
                "file": owl_file.name,
                "error": str(e),
            })
            print(f"ERROR ({e})")

    print(f"\nDone. Writing report to {OUTPUT_REPORT} ...")
    write_report(owl_files, passed, failed_analysis, with_pitfalls)
    print("Report written.")


def write_report(owl_files, passed, failed_analysis, with_pitfalls):
    lines = []
    total = len(owl_files)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ── Header ──────────────────────────────────────────────────────────────
    lines += [
        "# OOPS! Pitfall Analysis Report",
        "",
        f"**Generated:** {now}  ",
        f"**Ontologies analysed:** {total}  ",
        f"**Path:** `data/output/ontologies`",
        "",
        "---",
        "",
        "## Summary",
        "",
        f"| Result | Count |",
        f"|--------|-------|",
        f"| ✅ Passed (no pitfalls) | {len(passed)} |",
        f"| ⚠️ Pitfalls found | {len(with_pitfalls)} |",
        f"| ❌ Unable to analyse | {len(failed_analysis)} |",
        f"| **Total** | **{total}** |",
        "",
        "---",
        "",
    ]

    # ── Passed ───────────────────────────────────────────────────────────────
    lines += [
        "## ✅ Passed — No Pitfalls Detected",
        "",
    ]
    if passed:
        for name in passed:
            lines.append(f"- `{name}`")
    else:
        lines.append("_None_")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ── Unable to analyse ────────────────────────────────────────────────────
    lines += [
        "## ❌ Unable to Analyse",
        "",
    ]
    if failed_analysis:
        for entry in failed_analysis:
            lines.append(f"### `{entry['file']}`")
            lines.append("")
            lines.append(f"> **Error:** {entry['error']}")
            lines.append("")
    else:
        lines.append("_None_")
    lines.append("---")
    lines.append("")

    # ── Ontologies with pitfalls ─────────────────────────────────────────────
    lines += [
        "## ⚠️ Pitfalls Found",
        "",
    ]

    if not with_pitfalls:
        lines.append("_None_")
    else:
        for entry in with_pitfalls:
            pitfalls = entry["pitfalls"]
            name = entry["file"]

            # Count by severity
            counts = {"Critical": 0, "Important": 0, "Minor": 0}
            for p in pitfalls:
                imp = p.get("importance", "Unknown")
                if imp in counts:
                    counts[imp] += 1
                else:
                    counts.setdefault(imp, 0)
                    counts[imp] += 1

            lines.append(f"### `{name}`")
            lines.append("")

            # Severity summary table
            lines += [
                "#### Severity Summary",
                "",
                "| Severity | Count |",
                "|----------|-------|",
                f"| 🔴 Critical | {counts.get('Critical', 0)} |",
                f"| 🟠 Important | {counts.get('Important', 0)} |",
                f"| 🟡 Minor | {counts.get('Minor', 0)} |",
                f"| **Total** | **{entry['pitfall_count']}** |",
                "",
            ]

            # Detailed findings, sorted by severity then code
            lines.append("#### Detailed Findings")
            lines.append("")

            sorted_pitfalls = sorted(
                pitfalls,
                key=lambda p: (
                    IMPORTANCE_ORDER.get(p.get("importance", "Unknown"), 99),
                    p.get("code", ""),
                ),
            )

            for p in sorted_pitfalls:
                imp = p.get("importance", "Unknown")
                icon = {"Critical": "🔴", "Important": "🟠", "Minor": "🟡"}.get(imp, "⚪")

                lines.append(
                    f"##### {icon} {p['code']} — {p['name']} `[{imp}]`"
                )
                lines.append("")
                lines.append(f"**Description:** {p['description']}")
                lines.append("")
                lines.append(f"**Affected elements:** {p['num_affected']}")

                lines.append("")

            lines.append("---")
            lines.append("")

    OUTPUT_REPORT.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    run()
