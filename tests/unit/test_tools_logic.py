"""Unit tests for tool-layer logic that previously produced silently-wrong results.

These cover the class of bug found in audit: status flags decoupled from data,
error states collapsed into benign states, and code-normalization gaps.
"""
from unittest.mock import patch

from src.tools.utilities import explain_pitfall
from src.tools import composite


# --- explain_pitfall zero-padding (bug ②) --------------------------------

def test_explain_pitfall_single_digit_forms_resolve():
    """P8, 8, p8 must all resolve to the padded P08 catalog entry."""
    for form in ["P8", "8", "p8", "P08", " 8 "]:
        result = explain_pitfall(pitfall_code=form)
        assert result["success"] is True, f"{form!r} should resolve to P08"
        assert result["data"]["code"] == "P08"


def test_explain_pitfall_all_single_digit_codes_reachable():
    for n in range(1, 10):
        result = explain_pitfall(pitfall_code=str(n))
        assert result["success"] is True, f"P0{n} unreachable via '{n}'"
        assert result["data"]["code"] == f"P0{n}"


def test_explain_pitfall_unknown_still_fails():
    assert explain_pitfall(pitfall_code="P99")["success"] is False
    assert explain_pitfall(pitfall_code="99")["success"] is False


# --- validate_batch: success reflects ALL checks, not just syntax (bug ⑤) --

def test_validate_batch_success_false_when_reasoning_inconsistent():
    inconsistent = {"is_consistent": False, "error": None, "inconsistent_classes": [], "reasoner": "hermit"}
    with patch.object(composite, "resolve_folder", return_value=_FakeFolder(["a.owl"])), \
         patch.object(composite.Path, "read_text", return_value="@prefix : <#> ."), \
         patch.object(composite, "_validate_syntax", return_value={"valid": True, "triple_count": 1, "error": None}), \
         patch.object(composite, "content_to_rdfxml_file", return_value="/tmp/fake.xml"), \
         patch.object(composite, "run_reasoner", return_value=inconsistent), \
         patch.object(composite.Path, "unlink"):
        out = composite.validate_batch(folder_path="/x", checks=["syntax", "reasoning"])
    assert out["success"] is False


def test_validate_batch_success_false_on_empty_folder():
    with patch.object(composite, "resolve_folder", return_value=_FakeFolder([])):
        out = composite.validate_batch(folder_path="/x")
    assert out["success"] is False
    assert out["data"]["aggregate"]["total"] == 0


def test_validate_batch_isolates_bad_file():
    """A file that errors becomes one failed row, not a whole-batch crash."""
    with patch.object(composite, "resolve_folder", return_value=_FakeFolder(["bad.owl"])), \
         patch.object(composite.Path, "read_text", side_effect=OSError("boom")):
        out = composite.validate_batch(folder_path="/x", checks=["syntax"])
    assert out["success"] is False
    assert out["data"]["aggregate"]["failed"] == 1


# --- oops_report: success reflects failures (bug ③) -----------------------

def test_oops_report_success_false_when_all_fail():
    def boom(*a, **k):
        raise RuntimeError("convert failed")
    with patch.object(composite, "resolve_folder", return_value=_FakeFolder(["a.owl", "b.owl"])), \
         patch.object(composite.Path, "read_text", return_value="x"), \
         patch.object(composite, "run_oops_scan", side_effect=boom):
        out = composite.oops_report(folder_path="/x")
    assert out["success"] is False
    assert out["data"]["summary"]["failed"] == 2


def test_oops_report_success_false_on_empty_folder():
    with patch.object(composite, "resolve_folder", return_value=_FakeFolder([])):
        out = composite.oops_report(folder_path="/x")
    assert out["success"] is False


class _FakeFolder:
    """Minimal folder stand-in whose glob returns fake Path-like files."""
    def __init__(self, names):
        self._names = names

    def glob(self, pattern):
        from pathlib import Path
        return [Path(f"/fake/{n}") for n in self._names]
