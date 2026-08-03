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


def test_run_reasoner_leaves_no_temp_file(tmp_path):
    """A completed run must not leak its JSON result temp file (regression ⑪)."""
    import glob
    import os
    import tempfile

    rdfxml = tmp_path / "o.xml"
    rdfxml.write_text('<?xml version="1.0"?><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"/>')
    tmpdir = tempfile.gettempdir()
    before = set(glob.glob(os.path.join(tmpdir, "tmp*.json")))
    run_reasoner(str(rdfxml), ReasonerType.HERMIT, timeout=15)
    after = set(glob.glob(os.path.join(tmpdir, "tmp*.json")))
    assert after - before == set(), "reasoner leaked a temp result file"
