import pytest
from src.core.formatter import format_syntax_result, format_oops_result, format_metrics_result


def test_format_syntax_valid():
    md = format_syntax_result({"valid": True, "error": None, "triple_count": 42})
    assert "Valid" in md or "✅" in md
    assert "42" in md


def test_format_syntax_invalid():
    md = format_syntax_result({"valid": False, "error": "bad token at line 5", "triple_count": 0})
    assert "Error" in md or "Invalid" in md or "❌" in md
    assert "bad token" in md


def test_format_oops_with_pitfalls():
    data = {
        "has_pitfalls": True,
        "pitfall_count": 2,
        "pitfalls": [
            {"code": "P08", "name": "Missing annotations", "importance": "Minor", "affected_elements": 5, "description": "..."},
            {"code": "P11", "name": "Missing domain or range", "importance": "Important", "affected_elements": 3, "description": "..."},
        ]
    }
    md = format_oops_result(data)
    assert "P08" in md
    assert "P11" in md
    assert "Minor" in md or "Important" in md


def test_format_oops_no_pitfalls():
    md = format_oops_result({"has_pitfalls": False, "pitfall_count": 0, "pitfalls": []})
    assert "✅" in md
    assert "No pitfalls" in md


def test_format_oops_error_not_rendered_as_clean():
    """A failed scan must NOT render as a green 'no pitfalls' line."""
    md = format_oops_result({"has_pitfalls": False, "pitfalls": [], "error": "Failed to convert to RDF/XML"})
    assert "✅" not in md
    assert "No pitfalls" not in md
    assert "failed" in md.lower()
    assert "Failed to convert" in md


def test_format_metrics_result():
    data = {
        "axiom_counts": {"triples": 100, "classes": 5, "object_properties": 3, "data_properties": 2, "annotation_properties": 0},
        "hierarchy": {"max_depth": 3, "avg_depth": 1.5, "max_branching": 2, "avg_branching": 1.5, "leaf_count": 3},
        "ontoqa_ratios": {"RR": 0.5, "AR": 0.4, "IR": 0.6},
        "axiom_complexity": {"axiom_diversity_score": 3, "construct_counts": {}},
        "lexical_quality": {"naming_strict_pct": 0.8, "naming_underscore_pct": 0.1, "naming_bad_pct": 0.1, "label_coverage": 0.9, "comment_coverage": 0.5},
    }
    md = format_metrics_result(data)
    assert "100" in md
    assert "RR" in md
