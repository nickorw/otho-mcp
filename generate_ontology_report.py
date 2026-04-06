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

import datetime
import json
import re
import statistics
from collections import deque
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
RDFS = rdflib.RDFS


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


def compute_hierarchy_metrics(g: rdflib.Graph) -> dict:
    """
    Compute class hierarchy depth and branching metrics from a parsed graph.

    Returns:
        max_depth        – longest subClassOf chain from any root to any leaf
        avg_depth        – mean depth across all named classes
        max_branching    – highest number of direct subclasses any class has
        avg_branching    – mean direct subclasses per class that has at least one
        leaf_count       – classes with no subclasses (bottom of the hierarchy)
    """
    # Collect all named owl:Class IRIs
    classes = set(g.subjects(RDF.type, OWL.Class))
    # Also pick up classes only declared via rdfs:subClassOf (common in compact Turtle)
    for s, _, o in g.triples((None, RDFS.subClassOf, None)):
        if isinstance(s, rdflib.URIRef):
            classes.add(s)
        if isinstance(o, rdflib.URIRef):
            classes.add(o)
    classes = {c for c in classes if isinstance(c, rdflib.URIRef)}

    if not classes:
        return {
            "max_depth": 0,
            "avg_depth": 0.0,
            "max_branching": 0,
            "avg_branching": 0.0,
            "leaf_count": 0,
        }

    # Build parent→children map (direct subClassOf only, ignore BNodes)
    children: dict[rdflib.URIRef, set] = {c: set() for c in classes}
    parents: dict[rdflib.URIRef, set] = {c: set() for c in classes}
    for child, _, parent in g.triples((None, RDFS.subClassOf, None)):
        if isinstance(child, rdflib.URIRef) and isinstance(parent, rdflib.URIRef):
            if child in children and parent in children:
                children[parent].add(child)
                parents[child].add(parent)

    # Compute depth via topological sort (longest path in DAG).
    # BFS with re-queuing on update correctly propagates through diamond hierarchies.
    depth_of: dict[rdflib.URIRef, int] = {c: 0 for c in classes}
    # In-degree for topological sort (count named parents within the graph)
    in_degree: dict[rdflib.URIRef, int] = {c: len(parents[c]) for c in classes}

    queue: deque = deque(c for c in classes if in_degree[c] == 0)
    visited_topo = set()

    while queue:
        node = queue.popleft()
        if node in visited_topo:
            continue
        visited_topo.add(node)
        for child in children[node]:
            depth_of[child] = max(depth_of[child], depth_of[node] + 1)
            in_degree[child] -= 1
            if in_degree[child] == 0:
                queue.append(child)

    # Classes unreachable from roots (cycles): assign depth 0 (already default)

    depths = list(depth_of.values())
    max_depth = max(depths)
    avg_depth = round(statistics.mean(depths), 2) if depths else 0.0

    # Branching
    branch_counts = [len(children[c]) for c in classes]
    max_branching = max(branch_counts) if branch_counts else 0
    nonzero_branches = [b for b in branch_counts if b > 0]
    avg_branching = round(statistics.mean(nonzero_branches), 2) if nonzero_branches else 0.0

    leaf_count = sum(1 for c in classes if not children[c])

    return {
        "max_depth": max_depth,
        "avg_depth": avg_depth,
        "max_branching": max_branching,
        "avg_branching": avg_branching,
        "leaf_count": leaf_count,
    }


def compute_ontoqa_ratios(g: rdflib.Graph, classes: int, object_properties: int, data_properties: int) -> dict:
    """
    Compute OntoQA structural ratios:
      RR (Relationship Richness) = |P| / (|H| + |P|)
      AR (Attribute Richness)    = |dp| / |C|
      IR (Inheritance Richness)  = total subClassOf triples / total named classes
    """
    # |H| = count of subClassOf triples between named URIs
    h = sum(
        1
        for s, _, o in g.triples((None, RDFS.subClassOf, None))
        if isinstance(s, rdflib.URIRef) and isinstance(o, rdflib.URIRef)
    )
    p = object_properties

    rr = round(p / (h + p), 4) if (h + p) > 0 else 0.0
    ar = round(data_properties / classes, 4) if classes > 0 else 0.0

    # IR: total subClassOf edges / total named classes  (h already counts them)
    total_classes = classes   # URIRef-filtered count passed in as parameter
    ir = round(h / total_classes, 4) if total_classes > 0 else 0.0

    return {"RR": rr, "AR": ar, "IR": ir}


def compute_axiom_complexity(g: rdflib.Graph) -> dict:
    """
    Count presence and frequency of advanced OWL constructs.
    Returns an axiom_diversity_score (0–10) and raw construct_counts.
    """
    constructs = {
        "someValuesFrom": OWL.someValuesFrom,
        "allValuesFrom": OWL.allValuesFrom,
        "disjointWith": OWL.disjointWith,
        "inverseOf": OWL.inverseOf,
        "equivalentClass": OWL.equivalentClass,
        "unionOf": OWL.unionOf,
        "intersectionOf": OWL.intersectionOf,
        "hasValue": OWL.hasValue,
    }
    counts: dict[str, int] = {}
    diversity = 0

    for name, pred in constructs.items():
        c = len(list(g.triples((None, pred, None))))
        counts[name] = c
        if c > 0:
            diversity += 1

    # Cardinality: sum of all three types, counted as one diversity point
    card_count = (
        len(list(g.triples((None, OWL.cardinality, None))))
        + len(list(g.triples((None, OWL.minCardinality, None))))
        + len(list(g.triples((None, OWL.maxCardinality, None))))
    )
    counts["cardinality"] = card_count
    if card_count > 0:
        diversity += 1

    return {
        "axiom_diversity_score": diversity,
        "construct_counts": counts,
    }


def compute_lexical_quality(g: rdflib.Graph) -> dict:
    """
    Compute naming convention adherence and rdfs:label/comment coverage.
    """
    upper_camel_strict  = re.compile(r"^[A-Z][A-Za-z0-9]*$")
    lower_camel_strict  = re.compile(r"^[a-z][A-Za-z0-9]*$")
    upper_camel_usc     = re.compile(r"^[A-Z][A-Za-z0-9_]*$")
    lower_camel_usc     = re.compile(r"^[a-z][A-Za-z0-9_]*$")

    classes = list(g.subjects(RDF.type, OWL.Class))
    obj_props = list(g.subjects(RDF.type, OWL.ObjectProperty))
    data_props = list(g.subjects(RDF.type, OWL.DatatypeProperty))
    ann_props = list(g.subjects(RDF.type, OWL.AnnotationProperty))

    # Build deduplicated mapping uri -> type; class takes precedence on collision
    entity_type: dict[rdflib.URIRef, str] = {}
    for e in (c for c in classes if isinstance(c, rdflib.URIRef)):
        entity_type[e] = "class"
    for e in (p for p in (obj_props + data_props + ann_props) if isinstance(p, rdflib.URIRef)):
        if e not in entity_type:
            entity_type[e] = "property"
    all_entities = list(entity_type.keys())
    total = len(all_entities)

    if total == 0:
        return {
            "naming_strict_pct": 0.0,
            "naming_underscore_pct": 0.0,
            "naming_bad_pct": 0.0,
            "label_coverage": 0.0,
            "comment_coverage": 0.0,
        }

    # Naming convention — three categories
    naming_strict = 0
    naming_with_underscore = 0
    naming_bad = 0
    for e, etype in entity_type.items():
        local = str(e).split("#")[-1].split("/")[-1]
        if etype == "class":
            strict_ok = bool(upper_camel_strict.match(local))
            usc_ok    = bool(upper_camel_usc.match(local))
        else:
            strict_ok = bool(lower_camel_strict.match(local))
            usc_ok    = bool(lower_camel_usc.match(local))

        if strict_ok:
            naming_strict += 1
        elif usc_ok:
            naming_with_underscore += 1
        else:
            naming_bad += 1

    # Label / comment coverage
    labels_count = sum(
        1 for e in all_entities
        if any(True for _ in g.objects(e, RDFS.label))
    )
    comments_count = sum(
        1 for e in all_entities
        if any(True for _ in g.objects(e, RDFS.comment))
    )

    return {
        "naming_strict_pct":     round(naming_strict / total, 4),
        "naming_underscore_pct": round(naming_with_underscore / total, 4),
        "naming_bad_pct":        round(naming_bad / total, 4),
        "label_coverage":        round(labels_count / total, 4),
        "comment_coverage":      round(comments_count / total, 4),
    }


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
        "max_depth": None,
        "avg_depth": None,
        "max_branching": None,
        "avg_branching": None,
        "leaf_count": None,
        "RR": None, "AR": None, "IR": None,
        "axiom_diversity_score": None,
        "construct_counts": None,
        "naming_strict_pct": None,
        "naming_underscore_pct": None,
        "naming_bad_pct": None,
        "label_coverage": None,
        "comment_coverage": None,
    }
    try:
        g = _parse_graph(owl_path)
        result["syntax_valid"] = True
        result["triples"] = len(g)
        result["classes"]               = sum(1 for s in g.subjects(RDF.type, OWL.Class)             if isinstance(s, rdflib.URIRef))
        result["object_properties"]     = sum(1 for s in g.subjects(RDF.type, OWL.ObjectProperty)   if isinstance(s, rdflib.URIRef))
        result["data_properties"]       = sum(1 for s in g.subjects(RDF.type, OWL.DatatypeProperty) if isinstance(s, rdflib.URIRef))
        result["annotation_properties"] = sum(1 for s in g.subjects(RDF.type, OWL.AnnotationProperty) if isinstance(s, rdflib.URIRef))
        result.update(compute_hierarchy_metrics(g))
        result.update(compute_ontoqa_ratios(g, result["classes"], result["object_properties"], result["data_properties"]))
        result.update(compute_axiom_complexity(g))
        result.update(compute_lexical_quality(g))
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
    owl_files = sorted((folder_path / "All").glob("*.owl"))
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
        # ── Hierarchy metrics (parsed) ──
        "max_depth_max": mx(valid_parses, "max_depth"),
        "max_depth_avg": avg(valid_parses, "max_depth"),
        "avg_depth_avg": avg(valid_parses, "avg_depth"),
        "max_branching_max": mx(valid_parses, "max_branching"),
        "avg_branching_avg": avg(valid_parses, "avg_branching"),
        "leaf_count_avg": avg(valid_parses, "leaf_count"),
        # ── OntoQA ratios ──
        "RR_avg": avg(valid_parses, "RR"),
        "AR_avg": avg(valid_parses, "AR"),
        "IR_avg": avg(valid_parses, "IR"),
        # ── Axiom complexity ──
        "axiom_diversity_avg": avg(valid_parses, "axiom_diversity_score"),
        "axiom_diversity_max": mx(valid_parses, "axiom_diversity_score"),
        # ── Lexical quality ──
        "naming_strict_avg":     avg(valid_parses, "naming_strict_pct"),
        "naming_underscore_avg": avg(valid_parses, "naming_underscore_pct"),
        "naming_bad_avg":        avg(valid_parses, "naming_bad_pct"),
        "label_coverage_avg": avg(valid_parses, "label_coverage"),
        "comment_coverage_avg": avg(valid_parses, "comment_coverage"),
        # ── Generator (from log data) ──
        "gen_success_rate": overall_g.get("success_rate"),
        "gen_avg_duration_s": round(overall_g.get("avg_duration_seconds") or 0, 1),
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
        f"> Date: {datetime.date.today().isoformat()}",
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
        ("Max inheritance depth", num(ref_full.get("max_depth"), 0), num(ref_trim.get("max_depth"), 0)),
        ("Avg inheritance depth", num(ref_full.get("avg_depth")), num(ref_trim.get("avg_depth"))),
        ("Max branching factor", num(ref_full.get("max_branching"), 0), num(ref_trim.get("max_branching"), 0)),
        ("Avg branching factor", num(ref_full.get("avg_branching")), num(ref_trim.get("avg_branching"))),
        ("Leaf classes", num(ref_full.get("leaf_count"), 0), num(ref_trim.get("leaf_count"), 0)),
        ("RR (Relationship Richness)", num(ref_full.get("RR"), 4), num(ref_trim.get("RR"), 4)),
        ("AR (Attribute Richness)", num(ref_full.get("AR"), 4), num(ref_trim.get("AR"), 4)),
        ("IR (Inheritance Richness)", num(ref_full.get("IR"), 4), num(ref_trim.get("IR"), 4)),
        ("Axiom Diversity Score", num(ref_full.get("axiom_diversity_score"), 0), num(ref_trim.get("axiom_diversity_score"), 0)),
        ("Naming: Strict CamelCase", num(ref_full.get("naming_strict_pct"), 4), num(ref_trim.get("naming_strict_pct"), 4)),
        ("Naming: Underscore Style", num(ref_full.get("naming_underscore_pct"), 4), num(ref_trim.get("naming_underscore_pct"), 4)),
        ("Naming: Non-conformant", num(ref_full.get("naming_bad_pct"), 4), num(ref_trim.get("naming_bad_pct"), 4)),
        ("Label Coverage", num(ref_full.get("label_coverage"), 4), num(ref_trim.get("label_coverage"), 4)),
        ("Comment Coverage", num(ref_full.get("comment_coverage"), 4), num(ref_trim.get("comment_coverage"), 4)),
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
        "### 2.2 Structural Metrics (avg / median)",
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
        "### 2.5 Hierarchy Complexity (avg across ontologies in folder)",
        "",
        "| Agent Type | Max Depth (max) | Max Depth (avg) | Avg Depth (avg) | Max Branching (max) | Avg Branching (avg) | Leaf Classes (avg) |",
        "|------------|:---------------:|:---------------:|:---------------:|:-------------------:|:-------------------:|:------------------:|",
    ]
    for fm in folder_metrics:
        lines.append(
            f"| **{fm['folder']}** "
            f"| {num(fm['max_depth_max'], 0)} "
            f"| {num(fm['max_depth_avg'])} "
            f"| {num(fm['avg_depth_avg'])} "
            f"| {num(fm['max_branching_max'], 0)} "
            f"| {num(fm['avg_branching_avg'])} "
            f"| {num(fm['leaf_count_avg'])} |"
        )

    lines += [
        "",
        "### 2.6 OntoQA Structural Ratios",
        "",
        "| Agent Type | RR avg | AR avg | IR avg |",
        "|------------|:------:|:------:|:------:|",
    ]
    for fm in folder_metrics:
        lines.append(
            f"| **{fm['folder']}** "
            f"| {num(fm['RR_avg'], 4)} "
            f"| {num(fm['AR_avg'], 4)} "
            f"| {num(fm['IR_avg'], 4)} |"
        )

    lines += [
        "",
        "### 2.7 Axiom Complexity & Lexical Quality",
        "",
        "| Agent Type | Axiom Diversity avg | Axiom Diversity max | Naming Strict avg | Naming Underscore avg | Naming Bad avg | Label Coverage avg | Comment Coverage avg |",
        "|------------|:-------------------:|:-------------------:|:-----------------:|:---------------------:|:--------------:|:------------------:|:--------------------:|",
    ]
    for fm in folder_metrics:
        lines.append(
            f"| **{fm['folder']}** "
            f"| {num(fm['axiom_diversity_avg'], 1)} "
            f"| {num(fm['axiom_diversity_max'], 0)} "
            f"| {num(fm['naming_strict_avg'], 4)} "
            f"| {num(fm['naming_underscore_avg'], 4)} "
            f"| {num(fm['naming_bad_avg'], 4)} "
            f"| {num(fm['label_coverage_avg'], 4)} "
            f"| {num(fm['comment_coverage_avg'], 4)} |"
        )

    lines += [
        "",
        "### 2.8 Generator Performance",
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
        file_count = len(sorted_files)

        def _flag(val) -> str:
            if val is True:  return "✅"
            if val is False: return "❌"
            return "—"

        # ── Table 1: Validation Results ──
        lines += [
            "**Validation Results**",
            "",
            f"| File ({file_count}) | Syntax | HermiT | Pellet | OOPS |",
            "|------|:------:|:------:|:------:|:----:|",
            f"| **TUMedifact (trimmed)** _(baseline)_ | ✅ | — | — | — |",
        ]
        for f in sorted_files:
            sx = "✅" if f["syntax_valid"] else "❌"
            lines.append(
                f"| `{f['filename']}` "
                f"| {sx} "
                f"| {_flag(f.get('val_hermit'))} "
                f"| {_flag(f.get('val_pellet'))} "
                f"| {_flag(f.get('val_oops'))} |"
            )

        # ── Table 2: Extracted Details ──
        lines += [
            "",
            "**Extracted Details**",
            "",
            f"| File ({file_count}) | Classes | Obj Props | Data Props | Ann Props | Triples | Max Depth | Avg Depth | Max Branch | Leaves | RR | AR | IR | Axiom Div. | Name Strict | Name Usc. | Name Bad | Label Cov. | Comment Cov. |",
            "|------|:-------:|:---------:|:----------:|:---------:|:-------:|:---------:|:---------:|:----------:|:------:|:--:|:--:|:--:|:----------:|:-----------:|:---------:|:--------:|:----------:|:------------:|",
            f"| **TUMedifact (trimmed)** _(baseline)_ "
            f"| **{rt.get('classes', 'N/A')}** "
            f"| **{rt.get('object_properties', 'N/A')}** "
            f"| **{rt.get('data_properties', 'N/A')}** "
            f"| **{rt.get('annotation_properties', 'N/A')}** "
            f"| **{rt.get('triples', 'N/A')}** "
            f"| **{rt.get('max_depth', 'N/A')}** "
            f"| **{rt.get('avg_depth', 'N/A')}** "
            f"| **{rt.get('max_branching', 'N/A')}** "
            f"| **{rt.get('leaf_count', 'N/A')}** "
            f"| **{rt.get('RR', 'N/A')}** "
            f"| **{rt.get('AR', 'N/A')}** "
            f"| **{rt.get('IR', 'N/A')}** "
            f"| **{rt.get('axiom_diversity_score', 'N/A')}** "
            f"| **{rt.get('naming_strict_pct', 'N/A')}** "
            f"| **{rt.get('naming_underscore_pct', 'N/A')}** "
            f"| **{rt.get('naming_bad_pct', 'N/A')}** "
            f"| **{rt.get('label_coverage', 'N/A')}** "
            f"| **{rt.get('comment_coverage', 'N/A')}** |",
        ]
        for f in sorted_files:
            lines.append(
                f"| `{f['filename']}` "
                f"| {f.get('classes', 'N/A')} "
                f"| {f.get('object_properties', 'N/A')} "
                f"| {f.get('data_properties', 'N/A')} "
                f"| {f.get('annotation_properties', 'N/A')} "
                f"| {f.get('triples', 'N/A')} "
                f"| {f.get('max_depth', 'N/A')} "
                f"| {f.get('avg_depth', 'N/A')} "
                f"| {f.get('max_branching', 'N/A')} "
                f"| {f.get('leaf_count', 'N/A')} "
                f"| {f.get('RR', 'N/A')} "
                f"| {f.get('AR', 'N/A')} "
                f"| {f.get('IR', 'N/A')} "
                f"| {f.get('axiom_diversity_score', 'N/A')} "
                f"| {f.get('naming_strict_pct', 'N/A')} "
                f"| {f.get('naming_underscore_pct', 'N/A')} "
                f"| {f.get('naming_bad_pct', 'N/A')} "
                f"| {f.get('label_coverage', 'N/A')} "
                f"| {f.get('comment_coverage', 'N/A')} |"
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

    ref_t_full = ref_full.get("triples") or None
    ref_t_trim = ref_trim.get("triples") or None
    ref_c_full = ref_full.get("classes") or None
    ref_c_trim = ref_trim.get("classes") or None

    for fm in folder_metrics:
        ta = fm["triples_avg"]
        ca = fm["classes_avg"]
        if ta is None or ca is None or ref_t_full is None or ref_c_full is None:
            lines.append(f"| **{fm['folder']}** | N/A | N/A | N/A | N/A | N/A | N/A |")
            continue
        dt_full = f"{ta - ref_t_full:+.0f}"
        dt_trim = f"{ta - ref_t_trim:+.0f}" if ref_t_trim is not None else "N/A"
        dc_full = f"{ca - ref_c_full:+.0f}"
        dc_trim = f"{ca - ref_c_trim:+.0f}" if ref_c_trim is not None else "N/A"
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
        f"_Reference — TUMedifact (full): {ref_t_full or 'N/A'} triples, {ref_c_full or 'N/A'} classes_  ",
        f"_Reference — TUMedifact (trimmed): {ref_t_trim or 'N/A'} triples, {ref_c_trim or 'N/A'} classes_",
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
    lines += [
        "",
        "---",
        "",
        "## 6. Metric Definitions",
        "",
        "### Structural Ratios (OntoQA Framework)",
        "- **RR (Relationship Richness)** = `|ObjectProperties| / (|subClassOf axioms| + |ObjectProperties|)`. Ratio of non-taxonomic to all relations. Higher values indicate a more interconnected graph rather than a flat taxonomy.",
        "- **AR (Attribute Richness)** = `|DatatypeProperties| / |Classes|`. Average number of data properties per class. Higher values indicate richer per-instance data modelling.",
        "- **IR (Inheritance Richness)** = `|subClassOf triples| / |all named classes|`. Average number of inheritance edges per class (including leaf classes). Distinct from Avg Branching which only considers parent classes.",
        "",
        "### Axiom Complexity",
        "- **Axiom Diversity Score** (0–10): Count of distinct advanced OWL constructs present in the ontology, out of: `owl:someValuesFrom`, `owl:allValuesFrom`, `owl:disjointWith`, `owl:inverseOf`, `owl:equivalentClass`, `owl:unionOf`, `owl:intersectionOf`, `owl:hasValue`, and cardinality restrictions (`owl:cardinality`, `owl:minCardinality`, `owl:maxCardinality`, counted as one). A score of 0 means the ontology uses only declarations and `rdfs:subClassOf`; a score of 10 means all construct types are present.",
        "",
        "### Lexical & Annotation Quality",
        "- **Naming: Strict CamelCase** (0.0–1.0): Fraction of named entities matching strict Semantic Web conventions — UpperCamelCase for classes (`^[A-Z][A-Za-z0-9]*$`), lowerCamelCase for properties (`^[a-z][A-Za-z0-9]*$`). No underscores.",
        "- **Naming: Underscore Style** (0.0–1.0): Fraction that follow camelCase with underscores (e.g. `Cl_Invoice`), a common prefix-based variation that would pass if underscores are allowed but failed the strict check.",
        "- **Naming: Non-conformant** (0.0–1.0): Fraction that match neither pattern. The three fractions sum to 1.0.",
        "- **Label Coverage** (0.0–1.0): Fraction of named entities (classes + all property types) that have at least one `rdfs:label` triple. 1.0 = fully labelled.",
        "- **Comment Coverage** (0.0–1.0): Fraction of named entities that have at least one `rdfs:comment` triple. 1.0 = fully documented.",
        "",
        "### Hierarchy Metrics",
        "- **Max Depth**: Length of the longest `rdfs:subClassOf` chain from a root class (no parent) to a leaf class. Computed via BFS.",
        "- **Avg Depth**: Mean depth across all named classes.",
        "- **Max Branching**: Highest number of direct subclasses any single class has.",
        "- **Avg Branching**: Mean number of direct subclasses per class, computed only over classes that have at least one child (excludes leaf classes).",
        "- **Leaf Classes**: Count of classes with no direct subclasses.",
        "",
    ]

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
