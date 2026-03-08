#!/usr/bin/env python3
"""
Generates a comprehensive ontology quality report for all generated ontologies
in data/FinalResults/Ontologies, organized by folder (agent type), and
compares them against the two reference ontologies (TUMedifact full and trimmed).

Metrics per ontology:
  - Syntax validity (rdflib parse success)
  - Reasoner consistency (HermiT & Pellet from log_analysis_data.json)
  - OOPS pitfalls (from log_analysis_data.json)
  - Axiom count (triples)
  - Class count
  - Object property count
  - Data property count
  - Annotation property count

Output: data/FinalResults/ontology_report.md  (and a .json summary)
"""

import json
import statistics
from pathlib import Path

import rdflib

# ──────────────────────────────────────────────────────────────────────────────
# Paths
# ──────────────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
ONTOLOGIES_DIR = BASE_DIR / "data" / "FinalResults" / "Ontologies"
REFERENCE_DIR = BASE_DIR / "data" / "TUMedifact"
OUTPUT_DIR = BASE_DIR / "data" / "FinalResults"

FOLDERS = ["workflow", "singleAgent", "dualAgent", "triAgent"]

REFERENCE_ONTOLOGIES = {
    "TUMedifact (full)": REFERENCE_DIR / "TUMedifact.owl",
    "TUMedifact (trimmed)": REFERENCE_DIR / "TUMedifact_trimmed.owl",
}

OWL = rdflib.OWL
RDF = rdflib.RDF


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _parse_graph(owl_path: Path) -> rdflib.Graph:
    """Parse an OWL/TTL file, trying Turtle first then RDF/XML."""
    g = rdflib.Graph()
    try:
        g.parse(str(owl_path), format="turtle")
        return g
    except Exception:
        pass
    g = rdflib.Graph()
    g.parse(str(owl_path), format="xml")
    return g


def parse_ontology_metrics(owl_path: Path) -> dict:
    """Parse an OWL/TTL file and return structural metrics."""
    result = {
        "syntax_valid": False,
        "parse_error": None,
        "triples": 0,
        "classes": 0,
        "object_properties": 0,
        "data_properties": 0,
        "annotation_properties": 0,
    }
    try:
        g = _parse_graph(owl_path)
        result["syntax_valid"] = True
        result["triples"] = len(g)
        result["classes"] = len(list(g.subjects(RDF.type, OWL.Class)))
        result["object_properties"] = len(list(g.subjects(RDF.type, OWL.ObjectProperty)))
        result["data_properties"] = len(list(g.subjects(RDF.type, OWL.DatatypeProperty)))
        result["annotation_properties"] = len(list(g.subjects(RDF.type, OWL.AnnotationProperty)))
    except Exception as e:
        result["parse_error"] = str(e)
    return result


def load_log_analysis(folder_path: Path) -> dict:
    """Load pre-processed log_analysis_data.json from a folder."""
    log_file = folder_path / "log_analysis_data.json"
    if not log_file.exists():
        return {}
    with open(log_file) as f:
        return json.load(f)


def parse_per_run_validation(folder_path: Path) -> dict[str, dict]:
    """
    Parse the PER-RUN VALIDATION RESULTS table from log_analysis_report.txt.
    Returns a dict keyed by timestamp string (e.g. '20260301_215700') with
    keys: syntax, oops, hermit, pellet  (each True/False).
    """
    report_file = folder_path / "log_analysis_report.txt"
    if not report_file.exists():
        return {}

    results: dict[str, dict] = {}
    in_table = False
    for line in report_file.read_text(encoding="utf-8").splitlines():
        if "PER-RUN VALIDATION RESULTS" in line:
            in_table = True
            continue
        if not in_table:
            continue
        # Stop at the legend or separator
        if line.startswith("Legend:") or line.startswith("==="):
            break
        # Skip header / separator lines
        if "|" not in line or "Syntax" in line or line.strip().startswith("-"):
            continue
        # Parse data row:  "20260301_215700      |     ✓    |     ✓    |     ✓    |     ✓   "
        parts = [p.strip() for p in line.split("|")]
        parts = [p for p in parts if p]  # drop empty edges
        if len(parts) < 5:
            continue
        ts = parts[0].strip()
        def _bool(cell: str) -> bool:
            return "✓" in cell
        results[ts] = {
            "syntax": _bool(parts[1]),
            "oops":   _bool(parts[2]),
            "hermit": _bool(parts[3]),
            "pellet": _bool(parts[4]),
        }
    return results


def collect_folder_metrics(folder_name: str) -> dict:
    """Collect metrics for all ontologies in a folder, merging parsed + log data."""
    folder_path = ONTOLOGIES_DIR / folder_name
    owl_files = sorted(folder_path.glob("*.owl"))
    log_data = load_log_analysis(folder_path)

    va = log_data.get("validation_analysis", {})
    ga = log_data.get("generator_analysis", {})
    overall_v = va.get("overall", {})
    overall_g = ga.get("overall", {})
    reasoner = va.get("reasoner_analysis", {})
    oops = va.get("oops_analysis", {})
    timing = va.get("timing_analysis", {})

    # Load per-run pass/fail from the text report
    per_run_validation = parse_per_run_validation(folder_path)

    # Parse each ontology for structural metrics, merging validation results
    per_file = []
    for owl in owl_files:
        m = parse_ontology_metrics(owl)
        m["filename"] = owl.name
        # Extract timestamp from filename (last two underscore-separated tokens without extension)
        # e.g. EDIFACT_ontology_20260301_215700.owl  →  20260301_215700
        stem_parts = owl.stem.split("_")
        ts = "_".join(stem_parts[-2:]) if len(stem_parts) >= 2 else ""
        val = per_run_validation.get(ts, {})
        m["val_syntax"] = val.get("syntax")   # may be None if not found
        m["val_oops"]   = val.get("oops")
        m["val_hermit"] = val.get("hermit")
        m["val_pellet"] = val.get("pellet")
        per_file.append(m)

    # Aggregate structural metrics
    valid_parses = [f for f in per_file if f["syntax_valid"]]
    count = len(per_file)

    def avg(lst, key):
        vals = [x[key] for x in lst if x.get(key) is not None]
        return round(statistics.mean(vals), 1) if vals else None

    def med(lst, key):
        vals = [x[key] for x in lst if x.get(key) is not None]
        return round(statistics.median(vals), 1) if vals else None

    def mn(lst, key):
        vals = [x[key] for x in lst if x.get(key) is not None]
        return min(vals) if vals else None

    def mx(lst, key):
        vals = [x[key] for x in lst if x.get(key) is not None]
        return max(vals) if vals else None

    return {
        "folder": folder_name,
        "ontology_count": count,
        # ── Syntax ──
        "syntax_valid_count": len(valid_parses),
        "syntax_valid_rate": overall_v.get("syntax_valid_rate", round(len(valid_parses) / count * 100, 1) if count else 0),
        # ── Reasoner (from log data) ──
        "hermit_consistent_rate": reasoner.get("hermit_consistent_rate"),
        "pellet_consistent_rate": reasoner.get("pellet_consistent_rate"),
        "both_consistent_rate": reasoner.get("both_consistent_rate"),
        "hermit_inconsistent_classes": reasoner.get("hermit_inconsistent_classes", []),
        "pellet_inconsistent_classes": reasoner.get("pellet_inconsistent_classes", []),
        # ── OOPS (from log data) ──
        "oops_passed_rate": overall_v.get("oops_passed_rate"),
        "oops_no_critical_important_rate": overall_v.get("oops_no_critical_important_rate"),
        "total_pitfall_occurrences": oops.get("total_pitfall_occurrences"),
        "unique_pitfalls": oops.get("unique_pitfalls"),
        "most_common_pitfalls": oops.get("most_common_pitfalls", []),
        # ── Structural metrics (parsed) ──
        "triples_avg": avg(valid_parses, "triples"),
        "triples_median": med(valid_parses, "triples"),
        "triples_min": mn(valid_parses, "triples"),
        "triples_max": mx(valid_parses, "triples"),
        "classes_avg": avg(valid_parses, "classes"),
        "classes_median": med(valid_parses, "classes"),
        "classes_min": mn(valid_parses, "classes"),
        "classes_max": mx(valid_parses, "classes"),
        "object_props_avg": avg(valid_parses, "object_properties"),
        "object_props_median": med(valid_parses, "object_properties"),
        "data_props_avg": avg(valid_parses, "data_properties"),
        "data_props_median": med(valid_parses, "data_properties"),
        "annotation_props_avg": avg(valid_parses, "annotation_properties"),
        "annotation_props_median": med(valid_parses, "annotation_properties"),
        # ── Generator (from log data) ──
        "gen_success_rate": overall_g.get("success_rate"),
        "gen_avg_duration_s": round(overall_g.get("avg_duration_seconds", 0), 1),
        "gen_avg_iterations": overall_g.get("avg_iterations"),
        "gen_pitfalls_during_gen": ga.get("pitfalls_analysis", {}).get("total_pitfall_occurrences"),
        # ── Timing ──
        "hermit_avg_s": timing.get("hermit_avg_seconds"),
        "pellet_avg_s": timing.get("pellet_avg_seconds"),
        # ── Per-file detail ──
        "per_file": per_file,
    }


def collect_reference_metrics() -> dict:
    """Collect metrics for both reference ontologies."""
    results = {}
    for label, path in REFERENCE_ONTOLOGIES.items():
        m = parse_ontology_metrics(path)
        m["filename"] = path.name
        results[label] = m
    return results


# ──────────────────────────────────────────────────────────────────────────────
# Markdown report
# ──────────────────────────────────────────────────────────────────────────────

def pct(v) -> str:
    if v is None:
        return "N/A"
    return f"{v:.1f}%"


def num(v, decimals=1) -> str:
    if v is None:
        return "N/A"
    if isinstance(v, float):
        return f"{v:.{decimals}f}"
    return str(v)


def build_markdown(folder_metrics: list[dict], ref_metrics: dict) -> str:
    lines = []

    lines += [
        "# Ontology Quality Report",
        "",
        "> Generated automatically from `generate_ontology_report.py`  ",
        f"> Date: {Path(__file__).parent}",
        "",
        "---",
        "",
        "## 1. Reference Ontologies (TUMedifact)",
        "",
        "These two ontologies serve as the baseline for comparison.",
        "",
        "| Metric | TUMedifact (full) | TUMedifact (trimmed) |",
        "|--------|:-----------------:|:--------------------:|",
    ]

    ref_full = ref_metrics.get("TUMedifact (full)", {})
    ref_trim = ref_metrics.get("TUMedifact (trimmed)", {})

    rows = [
        ("Syntax valid", "✅" if ref_full.get("syntax_valid") else "❌", "✅" if ref_trim.get("syntax_valid") else "❌"),
        ("Triples (axioms)", num(ref_full.get("triples"), 0), num(ref_trim.get("triples"), 0)),
        ("Classes", num(ref_full.get("classes"), 0), num(ref_trim.get("classes"), 0)),
        ("Object properties", num(ref_full.get("object_properties"), 0), num(ref_trim.get("object_properties"), 0)),
        ("Data properties", num(ref_full.get("data_properties"), 0), num(ref_trim.get("data_properties"), 0)),
        ("Annotation properties", num(ref_full.get("annotation_properties"), 0), num(ref_trim.get("annotation_properties"), 0)),
    ]
    for label, v_full, v_trim in rows:
        lines.append(f"| {label} | {v_full} | {v_trim} |")

    lines += [
        "",
        "---",
        "",
        "## 2. Generated Ontologies — Summary by Agent Type",
        "",
        "Each folder contains 20 generated ontologies for the EDIFACT domain story.",
        "",
    ]

    # ── Summary table ──
    lines += [
        "### 2.1 High-level Validation Summary",
        "",
        "| Agent Type | N | Syntax Valid | HermiT Consistent | Pellet Consistent | OOPS Passed | No Critical Pitfalls |",
        "|------------|:-:|:------------:|:-----------------:|:-----------------:|:-----------:|:--------------------:|",
    ]
    for fm in folder_metrics:
        lines.append(
            f"| **{fm['folder']}** "
            f"| {fm['ontology_count']} "
            f"| {pct(fm['syntax_valid_rate'])} "
            f"| {pct(fm['hermit_consistent_rate'])} "
            f"| {pct(fm['pellet_consistent_rate'])} "
            f"| {pct(fm['oops_passed_rate'])} "
            f"| {pct(fm['oops_no_critical_important_rate'])} |"
        )

    lines += [
        "",
        "### 2.2 Structural Metrics (avg / median / min / max)",
        "",
        "| Agent Type | Triples avg | Triples med | Classes avg | Classes med | Obj Props avg | Data Props avg | Ann Props avg |",
        "|------------|:-----------:|:-----------:|:-----------:|:-----------:|:-------------:|:--------------:|:-------------:|",
    ]
    for fm in folder_metrics:
        lines.append(
            f"| **{fm['folder']}** "
            f"| {num(fm['triples_avg'])} "
            f"| {num(fm['triples_median'])} "
            f"| {num(fm['classes_avg'])} "
            f"| {num(fm['classes_median'])} "
            f"| {num(fm['object_props_avg'])} "
            f"| {num(fm['data_props_avg'])} "
            f"| {num(fm['annotation_props_avg'])} |"
        )

    lines += [
        "",
        "### 2.3 Structural Range (min–max)",
        "",
        "| Agent Type | Triples min | Triples max | Classes min | Classes max |",
        "|------------|:-----------:|:-----------:|:-----------:|:-----------:|",
    ]
    for fm in folder_metrics:
        lines.append(
            f"| **{fm['folder']}** "
            f"| {num(fm['triples_min'], 0)} "
            f"| {num(fm['triples_max'], 0)} "
            f"| {num(fm['classes_min'], 0)} "
            f"| {num(fm['classes_max'], 0)} |"
        )

    lines += [
        "",
        "### 2.4 OOPS Pitfall Summary",
        "",
        "| Agent Type | Total Pitfall Occurrences | Unique Pitfalls | Most Common |",
        "|------------|:-------------------------:|:---------------:|-------------|",
    ]
    for fm in folder_metrics:
        common = ", ".join(f"{p[0]} (×{p[1]})" for p in fm.get("most_common_pitfalls", [])) or "None"
        lines.append(
            f"| **{fm['folder']}** "
            f"| {num(fm['total_pitfall_occurrences'], 0)} "
            f"| {num(fm['unique_pitfalls'], 0)} "
            f"| {common} |"
        )

    lines += [
        "",
        "### 2.5 Generator Performance",
        "",
        "| Agent Type | Gen Success Rate | Avg Duration (s) | Avg Iterations | Pitfalls During Gen |",
        "|------------|:----------------:|:----------------:|:--------------:|:-------------------:|",
    ]
    for fm in folder_metrics:
        lines.append(
            f"| **{fm['folder']}** "
            f"| {pct(fm['gen_success_rate'])} "
            f"| {num(fm['gen_avg_duration_s'])} "
            f"| {num(fm['gen_avg_iterations'])} "
            f"| {num(fm['gen_pitfalls_during_gen'], 0)} |"
        )

    lines += [
        "",
        "---",
        "",
        "## 3. Per-Folder Detail",
        "",
    ]

    for fm in folder_metrics:
        lines += [
            f"### 3.{FOLDERS.index(fm['folder']) + 1} {fm['folder']}",
            "",
        ]

        # Inconsistent classes
        h_inc = fm.get("hermit_inconsistent_classes", [])
        p_inc = fm.get("pellet_inconsistent_classes", [])
        if h_inc:
            lines.append(f"**HermiT inconsistent classes ({len(h_inc)}):** " + ", ".join(f"`{c}`" for c in h_inc[:10]) + (" ..." if len(h_inc) > 10 else ""))
            lines.append("")
        if p_inc:
            lines.append(f"**Pellet inconsistent classes ({len(p_inc)}):** " + ", ".join(f"`{c}`" for c in p_inc[:10]) + (" ..." if len(p_inc) > 10 else ""))
            lines.append("")

        # Per-file table — sorted by class count descending
        def _sort_key(f):
            return f.get("classes", 0) if f.get("syntax_valid") else -1

        sorted_files = sorted(fm["per_file"], key=_sort_key, reverse=True)

        rt = ref_metrics.get("TUMedifact (trimmed)", {})
        lines += [
            "| File | Syntax | HermiT | Pellet | OOPS | Classes | Obj Props | Data Props | Ann Props | Triples |",
            "|------|:------:|:------:|:------:|:----:|:-------:|:---------:|:----------:|:---------:|:-------:|",
            f"| **TUMedifact (trimmed)** _(baseline)_ "
            f"| ✅ | — | — | — "
            f"| **{rt.get('classes', 'N/A')}** "
            f"| **{rt.get('object_properties', 'N/A')}** "
            f"| **{rt.get('data_properties', 'N/A')}** "
            f"| **{rt.get('annotation_properties', 'N/A')}** "
            f"| **{rt.get('triples', 'N/A')}** |",
        ]
        for f in sorted_files:
            def _flag(val) -> str:
                if val is True:   return "✅"
                if val is False:  return "❌"
                return "—"

            sx = "✅" if f["syntax_valid"] else f"❌"
            lines.append(
                f"| `{f['filename']}` "
                f"| {sx} "
                f"| {_flag(f.get('val_hermit'))} "
                f"| {_flag(f.get('val_pellet'))} "
                f"| {_flag(f.get('val_oops'))} "
                f"| {f.get('classes', 'N/A')} "
                f"| {f.get('object_properties', 'N/A')} "
                f"| {f.get('data_properties', 'N/A')} "
                f"| {f.get('annotation_properties', 'N/A')} "
                f"| {f.get('triples', 'N/A')} |"
            )
        lines.append("")

    # ── Comparison section ──
    lines += [
        "---",
        "",
        "## 4. Comparison with Reference Ontologies",
        "",
        "Values compared against **TUMedifact (full)** and **TUMedifact (trimmed)**.",
        "",
        "| Agent Type | Triples avg | vs Full | vs Trimmed | Classes avg | vs Full | vs Trimmed |",
        "|------------|:-----------:|:-------:|:----------:|:-----------:|:-------:|:----------:|",
    ]

    ref_t_full = ref_full.get("triples", 0) or 1
    ref_t_trim = ref_trim.get("triples", 0) or 1
    ref_c_full = ref_full.get("classes", 0) or 1
    ref_c_trim = ref_trim.get("classes", 0) or 1

    for fm in folder_metrics:
        ta = fm["triples_avg"] or 0
        ca = fm["classes_avg"] or 0
        dt_full = f"{ta - ref_t_full:+.0f}"
        dt_trim = f"{ta - ref_t_trim:+.0f}"
        dc_full = f"{ca - ref_c_full:+.0f}"
        dc_trim = f"{ca - ref_c_trim:+.0f}"
        lines.append(
            f"| **{fm['folder']}** "
            f"| {num(ta)} "
            f"| {dt_full} "
            f"| {dt_trim} "
            f"| {num(ca)} "
            f"| {dc_full} "
            f"| {dc_trim} |"
        )

    lines += [
        "",
        f"_Reference — TUMedifact (full): {ref_t_full} triples, {ref_c_full} classes_  ",
        f"_Reference — TUMedifact (trimmed): {ref_t_trim} triples, {ref_c_trim} classes_",
        "",
        "---",
        "",
        "## 5. Key Observations",
        "",
    ]

    # Auto-generate observations
    obs = []
    for fm in folder_metrics:
        hr = fm.get("hermit_consistent_rate")
        if hr is not None and hr < 100:
            obs.append(f"- **{fm['folder']}**: HermiT consistency rate is {hr:.1f}% — {fm['ontology_count'] - round(hr * fm['ontology_count'] / 100)} ontologies are inconsistent.")
        if fm.get("total_pitfall_occurrences"):
            obs.append(f"- **{fm['folder']}**: {fm['total_pitfall_occurrences']} OOPS pitfall occurrence(s) detected across runs (most common: {', '.join(p[0] for p in fm['most_common_pitfalls'])}).")
        if fm.get("classes_avg") and ref_c_full:
            ratio = fm["classes_avg"] / ref_c_full
            obs.append(f"- **{fm['folder']}**: Average class count is {fm['classes_avg']:.1f} ({ratio:.1%} of reference full ontology's {ref_c_full} classes).")

    if not obs:
        obs = ["- All generated ontologies are syntactically valid across all agent types."]

    lines += obs
    lines += [""]

    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main():
    print("Collecting reference ontology metrics...")
    ref_metrics = collect_reference_metrics()
    for label, m in ref_metrics.items():
        print(f"  {label}: {m['triples']} triples, {m['classes']} classes, syntax={m['syntax_valid']}")

    print("\nCollecting folder metrics...")
    folder_metrics = []
    for folder in FOLDERS:
        folder_path = ONTOLOGIES_DIR / folder
        if not folder_path.exists():
            print(f"  Skipping {folder} (not found)")
            continue
        print(f"  Processing {folder}...")
        fm = collect_folder_metrics(folder)
        folder_metrics.append(fm)
        print(f"    {fm['ontology_count']} ontologies, syntax_valid={fm['syntax_valid_rate']}%, "
              f"hermit={fm['hermit_consistent_rate']}%, classes_avg={fm['classes_avg']}")

    print("\nBuilding markdown report...")
    md = build_markdown(folder_metrics, ref_metrics)

    report_path = OUTPUT_DIR / "ontology_report.md"
    report_path.write_text(md, encoding="utf-8")
    print(f"  Written: {report_path}")

    # Also save raw JSON summary
    summary = {
        "reference_ontologies": ref_metrics,
        "folders": folder_metrics,
    }
    # Remove per_file from JSON to keep it manageable (it's in the md)
    for fm in summary["folders"]:
        fm.pop("per_file", None)
        fm.pop("hermit_inconsistent_classes", None)
        fm.pop("pellet_inconsistent_classes", None)

    json_path = OUTPUT_DIR / "ontology_report.json"
    with open(json_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"  Written: {json_path}")

    print("\nDone.")


if __name__ == "__main__":
    main()
