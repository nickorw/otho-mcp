"""Unit tests for file_resolver — path/content resolution contract."""
import pytest

from src.core.file_resolver import resolve_content, resolve_path


def test_resolve_content_returns_inline():
    assert resolve_content(owl_content="@prefix : <#> .") == "@prefix : <#> ."


def test_resolve_content_neither_raises():
    with pytest.raises(ValueError, match="Either file_path or owl_content"):
        resolve_content()


def test_resolve_content_both_raises():
    """Passing both must error, not silently ignore the file (regression ⑯)."""
    with pytest.raises(ValueError, match="not both"):
        resolve_content(file_path="/some/path.owl", owl_content="@prefix : <#> .")


def test_file_not_found_error_omits_container_path(tmp_path, monkeypatch):
    """FileNotFoundError must not leak the resolved container path to the caller."""
    monkeypatch.setenv("HOST_HOME", str(tmp_path))
    monkeypatch.setenv("HOST_MOUNT_PREFIX", str(tmp_path))
    # Reimport settings so the monkeypatched env takes effect
    import importlib
    import src.core.config as cfg_mod
    import src.core.file_resolver as fr_mod
    cfg_mod.settings = cfg_mod.Settings()
    importlib.reload(fr_mod)
    from src.core.file_resolver import resolve_content as rc

    nonexistent = str(tmp_path / "missing.owl")
    with pytest.raises(FileNotFoundError) as exc_info:
        rc(file_path=nonexistent)
    # Must NOT contain the container-internal "(resolved to ...)" detail
    assert "resolved to" not in str(exc_info.value)
