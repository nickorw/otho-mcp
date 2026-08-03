"""Unit tests for file_resolver — path/content resolution contract."""
import pytest

from src.core.file_resolver import resolve_content


def test_resolve_content_returns_inline():
    assert resolve_content(owl_content="@prefix : <#> .") == "@prefix : <#> ."


def test_resolve_content_neither_raises():
    with pytest.raises(ValueError, match="Either file_path or owl_content"):
        resolve_content()


def test_resolve_content_both_raises():
    """Passing both must error, not silently ignore the file (regression ⑯)."""
    with pytest.raises(ValueError, match="not both"):
        resolve_content(file_path="/some/path.owl", owl_content="@prefix : <#> .")
