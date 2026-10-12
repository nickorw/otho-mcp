"""Full ontology metrics computation."""

import re
import statistics
from collections import deque

import rdflib
from rdflib import Graph, OWL, RDF, RDFS

METRIC_DEFINITIONS = {
    "triples": "Total number of RDF triples in the ontology graph.",
    "classes": "Named OWL classes (owl:Class with URIRef subjects).",
    "object_properties": "Properties linking individuals to individuals (owl:ObjectProperty).",
    "data_properties": "Properties linking individuals to data values (owl:DatatypeProperty).",
    "annotation_properties": "Properties for metadata like labels and comments (owl:AnnotationProperty).",
    "max_depth": "Longest rdfs:subClassOf chain from any root class to any leaf class.",
    "avg_depth": "Mean depth across all named classes in the hierarchy.",
    "max_branching": "Highest number of direct subclasses any single class has.",
    "avg_branching": "Mean direct subclasses per class (for classes that have at least one).",
    "leaf_count": "Classes with no subclasses (bottom of the hierarchy).",
    "RR": "Relationship Richness = |ObjectProperties| / (|SubClassOf edges| + |ObjectProperties|). Higher means more non-hierarchical relationships.",
    "AR": "Attribute Richness = |DataProperties| / |Classes|. Higher means more data attributes per class.",
    "IR": "Inheritance Richness = |SubClassOf edges| / |Classes|. Higher means deeper/wider inheritance hierarchies.",
    "axiom_diversity_score": "Count (0-10) of distinct advanced OWL constructs used (someValuesFrom, allValuesFrom, disjointWith, inverseOf, equivalentClass, unionOf, intersectionOf, hasValue, cardinality).",
    "naming_strict_pct": "Percentage of entities following strict CamelCase (UpperCamel for classes, lowerCamel for properties).",
    "naming_underscore_pct": "Percentage of entities using underscores but otherwise following case conventions.",
    "naming_bad_pct": "Percentage of entities not following any recognized naming convention.",
    "label_coverage": "Fraction of entities that have an rdfs:label annotation.",
    "comment_coverage": "Fraction of entities that have an rdfs:comment annotation.",
}


def compute_metrics(content: str, format: str = "turtle") -> dict:
    """Compute all ontology metrics from content string."""
    g = Graph()
    g.parse(data=content, format=format)

    classes = sum(1 for s in g.subjects(RDF.type, OWL.Class) if isinstance(s, rdflib.URIRef))
    obj_props = sum(1 for s in g.subjects(RDF.type, OWL.ObjectProperty) if isinstance(s, rdflib.URIRef))
    data_props = sum(1 for s in g.subjects(RDF.type, OWL.DatatypeProperty) if isinstance(s, rdflib.URIRef))
    ann_props = sum(1 for s in g.subjects(RDF.type, OWL.AnnotationProperty) if isinstance(s, rdflib.URIRef))

    hierarchy = _compute_hierarchy_metrics(g)
    ontoqa = _compute_ontoqa_ratios(g, classes, obj_props, data_props)
    complexity = _compute_axiom_complexity(g)
    lexical = _compute_lexical_quality(g)

    return {
        "axiom_counts": {
            "triples": len(g),
            "classes": classes,
            "object_properties": obj_props,
            "data_properties": data_props,
            "annotation_properties": ann_props,
        },
        "hierarchy": hierarchy,
        "ontoqa_ratios": ontoqa,
        "axiom_complexity": complexity,
        "lexical_quality": lexical,
        "definitions": METRIC_DEFINITIONS,
    }


def _compute_hierarchy_metrics(g: Graph) -> dict:
    """Compute class hierarchy depth and branching metrics."""
    classes = set(g.subjects(RDF.type, OWL.Class))
    for s, _, o in g.triples((None, RDFS.subClassOf, None)):
        if isinstance(s, rdflib.URIRef):
            classes.add(s)
        if isinstance(o, rdflib.URIRef):
            classes.add(o)
    classes = {c for c in classes if isinstance(c, rdflib.URIRef)}

    if not classes:
        return {"max_depth": 0, "avg_depth": 0.0, "max_branching": 0, "avg_branching": 0.0, "leaf_count": 0}

    children: dict = {c: set() for c in classes}
    parents: dict = {c: set() for c in classes}
    for child, _, parent in g.triples((None, RDFS.subClassOf, None)):
        if isinstance(child, rdflib.URIRef) and isinstance(parent, rdflib.URIRef):
            if child in children and parent in children:
                children[parent].add(child)
                parents[child].add(parent)

    depth_of = {c: 0 for c in classes}
    in_degree = {c: len(parents[c]) for c in classes}
    queue = deque(c for c in classes if in_degree[c] == 0)
    visited = set()

    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        for child in children[node]:
            depth_of[child] = max(depth_of[child], depth_of[node] + 1)
            in_degree[child] -= 1
            if in_degree[child] == 0:
                queue.append(child)

    depths = list(depth_of.values())
    branch_counts = [len(children[c]) for c in classes]
    nonzero_branches = [b for b in branch_counts if b > 0]

    return {
        "max_depth": max(depths),
        "avg_depth": round(statistics.mean(depths), 2) if depths else 0.0,
        "max_branching": max(branch_counts) if branch_counts else 0,
        "avg_branching": round(statistics.mean(nonzero_branches), 2) if nonzero_branches else 0.0,
        "leaf_count": sum(1 for c in classes if not children[c]),
    }


def _compute_ontoqa_ratios(g: Graph, classes: int, obj_props: int, data_props: int) -> dict:
    """Compute OntoQA structural ratios: RR, AR, IR."""
    h = sum(1 for s, _, o in g.triples((None, RDFS.subClassOf, None))
            if isinstance(s, rdflib.URIRef) and isinstance(o, rdflib.URIRef))
    p = obj_props
    rr = round(p / (h + p), 4) if (h + p) > 0 else 0.0
    ar = round(data_props / classes, 4) if classes > 0 else 0.0
    ir = round(h / classes, 4) if classes > 0 else 0.0
    return {"RR": rr, "AR": ar, "IR": ir}


def _compute_axiom_complexity(g: Graph) -> dict:
    """Count advanced OWL constructs and compute diversity score."""
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
    counts = {}
    diversity = 0
    for name, pred in constructs.items():
        c = len(list(g.triples((None, pred, None))))
        counts[name] = c
        if c > 0:
            diversity += 1

    card_count = (
        len(list(g.triples((None, OWL.cardinality, None))))
        + len(list(g.triples((None, OWL.minCardinality, None))))
        + len(list(g.triples((None, OWL.maxCardinality, None))))
    )
    counts["cardinality"] = card_count
    if card_count > 0:
        diversity += 1

    return {"axiom_diversity_score": diversity, "construct_counts": counts}


def _compute_lexical_quality(g: Graph) -> dict:
    """Compute naming conventions and annotation coverage."""
    upper_camel_strict = re.compile(r"^[A-Z][A-Za-z0-9]*$")
    lower_camel_strict = re.compile(r"^[a-z][A-Za-z0-9]*$")
    upper_camel_usc = re.compile(r"^[A-Z][A-Za-z0-9_]*$")
    lower_camel_usc = re.compile(r"^[a-z][A-Za-z0-9_]*$")

    classes_list = list(g.subjects(RDF.type, OWL.Class))
    obj_props = list(g.subjects(RDF.type, OWL.ObjectProperty))
    data_props = list(g.subjects(RDF.type, OWL.DatatypeProperty))
    ann_props = list(g.subjects(RDF.type, OWL.AnnotationProperty))

    entity_type: dict = {}
    for e in (c for c in classes_list if isinstance(c, rdflib.URIRef)):
        entity_type[e] = "class"
    for e in (p for p in (obj_props + data_props + ann_props) if isinstance(p, rdflib.URIRef)):
        if e not in entity_type:
            entity_type[e] = "property"

    total = len(entity_type)
    if total == 0:
        return {"naming_strict_pct": 0.0, "naming_underscore_pct": 0.0, "naming_bad_pct": 0.0, "label_coverage": 0.0, "comment_coverage": 0.0}

    naming_strict = naming_usc = naming_bad = 0
    for e, etype in entity_type.items():
        local = str(e).split("#")[-1].split("/")[-1]
        if etype == "class":
            strict_ok = bool(upper_camel_strict.match(local))
            usc_ok = bool(upper_camel_usc.match(local))
        else:
            strict_ok = bool(lower_camel_strict.match(local))
            usc_ok = bool(lower_camel_usc.match(local))
        if strict_ok:
            naming_strict += 1
        elif usc_ok:
            naming_usc += 1
        else:
            naming_bad += 1

    labels = sum(1 for e in entity_type if any(True for _ in g.objects(e, RDFS.label)))
    comments = sum(1 for e in entity_type if any(True for _ in g.objects(e, RDFS.comment)))

    return {
        "naming_strict_pct": round(naming_strict / total, 4),
        "naming_underscore_pct": round(naming_usc / total, 4),
        "naming_bad_pct": round(naming_bad / total, 4),
        "label_coverage": round(labels / total, 4),
        "comment_coverage": round(comments / total, 4),
    }
