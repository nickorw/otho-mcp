"""Integration tests for MCP tools (require no Docker — test logic only)."""
import pytest
from pathlib import Path

from src.tools.validators import validate_syntax
from src.tools.utilities import ontology_metrics, convert_format, explain_pitfall

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures" / "ontologies"


@pytest.fixture
def sample_content():
    owl_files = sorted(FIXTURES_DIR.glob("*.owl"))
    if owl_files:
        return owl_files[0].read_text(encoding="utf-8")
    pytest.skip("No fixture ontologies available")


def test_validate_syntax_tool(sample_content):
    result = validate_syntax(owl_content=sample_content)
    assert "success" in result
    assert "markdown_summary" in result
    assert result["tool"] == "validate_syntax"


def test_ontology_metrics_tool(sample_content):
    result = ontology_metrics(owl_content=sample_content)
    assert result["success"] is True
    assert "axiom_counts" in result["data"]
    assert "definitions" in result["data"]


def test_convert_format_tool(sample_content):
    result = convert_format(owl_content=sample_content, source_format="turtle", target_format="xml")
    assert result["success"] is True
    assert "rdf" in result["data"]["content"].lower() or "RDF" in result["data"]["content"]


def test_explain_pitfall_known():
    result = explain_pitfall(pitfall_code="P08")
    assert result["success"] is True
    assert "P08" in result["data"]["code"]


def test_explain_pitfall_unknown():
    result = explain_pitfall(pitfall_code="P99")
    assert result["success"] is False
