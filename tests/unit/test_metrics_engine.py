import pytest
from src.engine.metrics_engine import compute_metrics

VALID_TURTLE = """@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

<http://example.org/onto> a owl:Ontology .
<http://example.org/onto#Person> a owl:Class ;
    rdfs:label "Person" ;
    rdfs:comment "A human being" .
<http://example.org/onto#Animal> a owl:Class ;
    rdfs:label "Animal" .
<http://example.org/onto#Pet> a owl:Class ;
    rdfs:subClassOf <http://example.org/onto#Animal> ;
    rdfs:label "Pet" .
<http://example.org/onto#hasName> a owl:DatatypeProperty ;
    rdfs:domain <http://example.org/onto#Person> ;
    rdfs:label "has name" .
<http://example.org/onto#owns> a owl:ObjectProperty ;
    rdfs:domain <http://example.org/onto#Person> ;
    rdfs:range <http://example.org/onto#Pet> ;
    rdfs:label "owns" .
"""


def test_compute_metrics_returns_all_categories():
    result = compute_metrics(VALID_TURTLE, format="turtle")
    assert "axiom_counts" in result
    assert "hierarchy" in result
    assert "ontoqa_ratios" in result
    assert "axiom_complexity" in result
    assert "lexical_quality" in result
    assert "definitions" in result


def test_axiom_counts_structure():
    result = compute_metrics(VALID_TURTLE, format="turtle")
    counts = result["axiom_counts"]
    assert counts["classes"] == 3
    assert counts["object_properties"] == 1
    assert counts["data_properties"] == 1
    assert counts["triples"] > 0


def test_hierarchy_metrics_structure():
    result = compute_metrics(VALID_TURTLE, format="turtle")
    h = result["hierarchy"]
    assert "max_depth" in h
    assert "avg_depth" in h
    assert "max_branching" in h
    assert "leaf_count" in h


def test_definitions_are_present():
    result = compute_metrics(VALID_TURTLE, format="turtle")
    defs = result["definitions"]
    assert "RR" in defs
    assert "axiom_diversity_score" in defs
    assert len(defs) >= 5
