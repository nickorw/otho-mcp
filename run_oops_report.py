#!/usr/bin/env python3
"""
Runs OOPS! pitfall scanner on all ontologies in
data/FinalResults/Ontologies/{dualAgent,singleAgent,triAgent,workflow}/All
and produces a unified Markdown report at oops_report.md, split by parent folder.
"""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.reviewers.reviewer import OopsPitfallReviewer
from src.utils.oops_parser import parse_oops_response

BASE_DIR = Path("data/FinalResults/Ontologies")
GROUPS = ["dualAgent", "singleAgent", "triAgent", "workflow"]
OUTPUT_REPORT = Path("oops_report.md")
OOPS_ENDPOINT = "http://localhost/OOPS/rest"
ALL_PITFALLS = ["2,3,4,5,6,7,8,10,11,12,13,19,20,21,22,24,25,26,27,28,29"]

IMPORTANCE_ORDER = {"Critical": 0, "Important": 1, "Minor": 2}


def _only_minor(pitfalls):
    return all(p.get("importance") == "Minor" for p in pitfalls)


def _append_pitfall_entry(lines, entry):
    """Append per-file pitfall detail block to lines."""
    pitfalls = entry["pitfalls"]
    name = entry["file"]

    counts = {"Critical": 0, "Important": 0, "Minor": 0}
    for p in pitfalls:
        imp = p.get("importance", "Unknown")
        counts[imp] = counts.get(imp, 0) + 1

    lines.append(f"#### `{name}`")
    lines.append("")
    lines += [
        "##### Severity Summary",
        "",
        "| Severity | Count |",
        "|----------|-------|",
        f"| 🔴 Critical | {counts.get('Critical', 0)} |",
        f"| 🟠 Important | {counts.get('Important', 0)} |",
        f"| 🟡 Minor | {counts.get('Minor', 0)} |",
        f"| **Total** | **{entry['pitfall_count']}** |",
        "",
        "##### Detailed Findings",
        "",
    ]

    sorted_pitfalls = sorted(
        pitfalls,
        key=lambda x: (
            IMPORTANCE_ORDER.get(x.get("importance", "Unknown"), 99),
            x.get("code", ""),
        ),
    )
    for p in sorted_pitfalls:
        imp = p.get("importance", "Unknown")
        icon = {"Critical": "🔴", "Important": "🟠", "Minor": "🟡"}.get(imp, "⚪")
        lines.append(f"###### {icon} {p['code']} — {p['name']} `[{imp}]`")
        lines.append("")
        lines.append(f"**Description:** {p['description']}")
        lines.append("")
        lines.append(f"**Affected elements:** {p['num_affected']}")
        lines.append("")


def analyse_files(reviewer, owl_files, group):
    """Run OOPS on a list of owl files. Returns (passed, failed, with_pitfalls)."""
    passed = []
    failed = []
    with_pitfalls = []

    for owl_file in owl_files:
        print(f"  Analysing {owl_file.name} ...", end=" ", flush=True)
        try:
            raw_xml = reviewer.review_owl_file(
                str(owl_file),
                pitfalls=ALL_PITFALLS,
                story_id=owl_file.stem,
                timestamp=group,
            )

            if (
                "wrong_execution" in raw_xml
                or "oops.linkeddata.es/data/wrong_execution" in raw_xml
            ):
                failed.append(
                    {
                        "file": owl_file.name,
                        "error": "OOPS could not analyse the ontology (wrong_execution response)",
                    }
                )
                print("UNABLE TO ANALYSE")
                continue

            result = parse_oops_response(raw_xml)

            if result.get("oops_error"):
                failed.append(
                    {
                        "file": owl_file.name,
                        "error": result.get("error", "Unknown error"),
                    }
                )
                print("ERROR (parse)")
            elif not result["has_pitfalls"]:
                passed.append(owl_file.name)
                print("PASSED")
            else:
                with_pitfalls.append(
                    {
                        "file": owl_file.name,
                        "pitfalls": result["pitfalls"],
                        "pitfall_count": result["pitfall_count"],
                    }
                )
                print(f"PITFALLS ({result['pitfall_count']})")

        except Exception as e:
            failed.append({"file": owl_file.name, "error": str(e)})
            print(f"ERROR ({e})")

    return passed, failed, with_pitfalls


def run():
    reviewer = OopsPitfallReviewer(endpoint=OOPS_ENDPOINT)

    group_results = {}
    for group in GROUPS:
        folder = BASE_DIR / group / "All"
        owl_files = sorted(folder.glob("*.owl"))
        if not owl_files:
            print(f"[WARN] No .owl files found in {folder}")
            group_results[group] = ([], [], [], [])
            continue

        print(f"\n── {group} ({len(owl_files)} ontologies) ──")
        passed, failed, with_pitfalls = analyse_files(reviewer, owl_files, group)
        group_results[group] = (owl_files, passed, failed, with_pitfalls)

    print(f"\nDone. Writing report to {OUTPUT_REPORT} ...")
    write_report(group_results)
    print("Report written.")


def _section_lines(group, owl_files, passed, failed, with_pitfalls):
    """Return Markdown lines for one group section."""
    lines = []
    total = len(owl_files)

    only_minor_count = sum(1 for e in with_pitfalls if _only_minor(e["pitfalls"]))
    serious_count = len(with_pitfalls) - only_minor_count

    lines += [
        f"## {group}",
        "",
        f"**Ontologies analysed:** {total}  ",
        f"**Path:** `{BASE_DIR / group / 'All'}`",
        "",
        "| Result | Count |",
        "|--------|-------|",
        f"| ✅ Passed | {len(passed)} |",
        f"| 🟡 Passed w/ Minor Pitfalls | {only_minor_count} |",
        f"| 🟠 Serious Pitfalls | {serious_count} |",
        f"| ❌ Failed | {len(failed)} |",
        f"| **Total** | **{total}** |",
        "",
    ]

    # Passed
    lines += ["### ✅ Passed — No Pitfalls Detected", ""]
    if passed:
        for name in passed:
            lines.append(f"- `{name}`")
    else:
        lines.append("_None_")
    lines.append("")

    # Unable to analyse
    lines += ["### ❌ Failed — Unable to Analyse", ""]
    if failed:
        for entry in failed:
            lines.append(f"#### `{entry['file']}`")
            lines.append("")
            lines.append(f"> **Error:** {entry['error']}")
            lines.append("")
    else:
        lines.append("_None_")
    lines.append("")

    # Pitfalls found — split by severity
    minor_only_entries = [e for e in with_pitfalls if _only_minor(e["pitfalls"])]
    serious_entries = [e for e in with_pitfalls if not _only_minor(e["pitfalls"])]

    lines += ["### 🟡 Passed w/ Minor Pitfalls", ""]
    if not minor_only_entries:
        lines.append("_None_")
        lines.append("")
    else:
        for entry in minor_only_entries:
            _append_pitfall_entry(lines, entry)

    lines += ["### 🟠 Serious Pitfalls", ""]
    if not serious_entries:
        lines.append("_None_")
        lines.append("")
    else:
        for entry in serious_entries:
            _append_pitfall_entry(lines, entry)

    lines += ["---", ""]
    return lines


def write_report(group_results):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    all_total = sum(len(r[0]) for r in group_results.values())
    all_passed = sum(len(r[1]) for r in group_results.values())
    all_failed = sum(len(r[2]) for r in group_results.values())
    all_only_minor = sum(
        sum(1 for e in r[3] if _only_minor(e["pitfalls"])) for r in group_results.values()
    )
    all_serious = sum(
        sum(1 for e in r[3] if not _only_minor(e["pitfalls"])) for r in group_results.values()
    )

    lines = [
        "# OOPS! Pitfall Analysis Report",
        "",
        f"**Generated:** {now}  ",
        f"**Ontologies analysed:** {all_total}  ",
        f"**Groups:** {', '.join(GROUPS)}",
        "",
        "---",
        "",
        "## Overall Summary",
        "",
        "| Group | Total | ✅ Passed | 🟡 Passed w/ Minor Pitfalls | 🟠 Serious Pitfalls | ❌ Failed |",
        "|-------|-------|-----------|----------------------------|---------------------|---------|",
    ]

    for group, (owl_files, passed, failed, with_pitfalls) in group_results.items():
        only_minor = sum(1 for e in with_pitfalls if _only_minor(e["pitfalls"]))
        serious = len(with_pitfalls) - only_minor
        lines.append(
            f"| {group} | {len(owl_files)} | {len(passed)} | {only_minor} | {serious} | {len(failed)} |"
        )

    lines += [
        f"| **Total** | **{all_total}** | **{all_passed}** | **{all_only_minor}** | **{all_serious}** | **{all_failed}** |",
        "",
        "---",
        "",
    ]

    for group, (owl_files, passed, failed, with_pitfalls) in group_results.items():
        lines += _section_lines(group, owl_files, passed, failed, with_pitfalls)

    OUTPUT_REPORT.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    run()
