import pytest
from src.engine.reasoner_engine import run_reasoner, ReasonerType


def test_run_reasoner_returns_expected_structure():
    """Test that result has expected keys even on error (no Java in test env)."""
    result = run_reasoner("/nonexistent/path.xml", ReasonerType.HERMIT, timeout=5)
    assert "reasoner" in result
    assert "is_consistent" in result
    assert "inconsistent_classes" in result
    assert "execution_time_seconds" in result
    assert "error" in result
    assert result["reasoner"] == "hermit"


def test_run_reasoner_invalid_path_returns_error():
    result = run_reasoner("/nonexistent/file.xml", ReasonerType.PELLET, timeout=5)
    assert result["is_consistent"] is False
    assert result["error"] is not None
