"""
Quick test script for Phase 2 reasoner validators.

Tests Hermit and Pellet reasoners using RDF/XML file from OOPS.
First converts a Turtle ontology to RDF/XML (simulating OOPS pipeline).
"""

from pathlib import Path

from rdflib import Graph

from src.reviewers.reasoner_validator import (
    HermitReasonerValidator,
    PelletReasonerValidator,
)
from src.utils.file_handler import save_text_file

# Load a recent FestS ontology
ontology_path = Path(
    "data/Resultset/FinalOntologiesForAnalysis/AgentV1_GPT4.1/FestS_ontology_20260110_133132.owl"
)

print("=" * 60)
print("TESTING PHASE 2 REASONER VALIDATORS")
print("=" * 60)
print(f"\nLoading ontology: {ontology_path.name}\n")

with open(ontology_path, "r", encoding="utf-8") as f:
    owl_content = f.read()

print(f"Ontology size: {len(owl_content)} characters")

# Convert Turtle to RDF/XML (simulating OOPS pipeline)
print("Converting Turtle to RDF/XML for reasoners...")
g = Graph()
g.parse(data=owl_content, format="turtle")
rdfxml_content = g.serialize(format="xml")
save_text_file("data/output/xml_combined_owl.xml", rdfxml_content)
print("✓ RDF/XML saved to data/output/xml_combined_owl.xml\n")

# Test Hermit
print("1️⃣  Testing Hermit Reasoner")
print("-" * 60)
hermit = HermitReasonerValidator()
hermit_result = hermit.validate()

print(f"Reasoner: {hermit_result['reasoner']}")
print(f"Consistent: {hermit_result['is_consistent']}")
print(f"Execution time: {hermit_result['execution_time_ms']}ms")
if hermit_result.get("error"):
    print(f"Error: {hermit_result['error']}")
if hermit_result.get("inconsistent_classes"):
    print(f"Inconsistent classes: {hermit_result['inconsistent_classes']}")
print()

# Test Pellet
print("2️⃣  Testing Pellet Reasoner")
print("-" * 60)
pellet = PelletReasonerValidator()
pellet_result = pellet.validate()

print(f"Reasoner: {pellet_result['reasoner']}")
print(f"Consistent: {pellet_result['is_consistent']}")
print(f"Execution time: {pellet_result['execution_time_ms']}ms")
if pellet_result.get("error"):
    print(f"Error: {pellet_result['error']}")
if pellet_result.get("inconsistent_classes"):
    print(f"Inconsistent classes: {pellet_result['inconsistent_classes']}")
print()

# Summary
print("=" * 60)
print("SUMMARY")
print("=" * 60)
print(
    f"Hermit: {'✓ PASSED' if hermit_result['is_consistent'] else '✗ FAILED'} ({hermit_result['execution_time_ms']}ms)"
)
print(
    f"Pellet: {'✓ PASSED' if pellet_result['is_consistent'] else '✗ FAILED'} ({pellet_result['execution_time_ms']}ms)"
)
total_time = hermit_result["execution_time_ms"] + pellet_result["execution_time_ms"]
print(f"Total reasoning time: {total_time}ms ({total_time / 1000:.2f}s)")
print("=" * 60)
