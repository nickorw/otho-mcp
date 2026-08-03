import os
import posixpath
from pathlib import Path
from src.core.config import settings


def _to_posix(file_path: str) -> str:
    """Normalize a host path to a POSIX-style absolute path.

    Handles macOS/Linux paths as-is and translates Windows paths:
      C:\\Users\\me\\o.owl  -> /c/Users/me/o.owl
      C:/Users/me/o.owl     -> /c/Users/me/o.owl
    """
    p = file_path.replace("\\", "/")
    # Windows drive letter, e.g. "C:/Users/..." -> "/c/Users/..."
    if len(p) >= 2 and p[1] == ":" and p[0].isalpha():
        p = f"/{p[0].lower()}{p[2:]}"
    return p


def _strip_home(posix_path: str) -> str:
    """Strip the host home prefix, returning the remainder relative to home.

    Returns a leading-slash-free remainder (e.g. "DevResearch/o.owl"), or the
    original path (minus leading slash) when no home prefix is configured/matched.
    """
    home = settings.host_home
    if home:
        home_posix = _to_posix(home).rstrip("/")
        if home_posix and (posix_path == home_posix or posix_path.startswith(home_posix + "/")):
            return posix_path[len(home_posix):].lstrip("/")
    return posix_path.lstrip("/")


def resolve_path(file_path: str) -> str:
    """Map a host OS path to the container-internal path under the mount prefix.

    Accepts macOS/Linux absolute paths, Windows paths, or an already
    mount-prefixed path. The host home directory (settings.host_home) is
    stripped and the remainder is anchored under host_mount_prefix (/host),
    which is where the user's home is bind-mounted. Prevents path traversal
    outside the mount boundary without following symlinks out of it.
    """
    prefix = settings.host_mount_prefix.rstrip("/")
    posix = _to_posix(file_path)

    if not posix.startswith("/"):
        raise ValueError(f"Only absolute paths are accepted, got: {file_path}")

    # Already inside the mount (back-compat / explicit container paths).
    if posix == prefix or posix.startswith(prefix + "/"):
        container_path = posix
    else:
        remainder = _strip_home(posix)
        container_path = f"{prefix}/{remainder}" if remainder else prefix

    # normpath collapses ".." lexically so traversal can't escape the mount,
    # without resolving symlinks (which on Docker Desktop point outside /host).
    normalized = posixpath.normpath(container_path)
    if normalized != prefix and not normalized.startswith(prefix + "/"):
        raise ValueError(f"Path escapes mount boundary: {file_path}")
    return normalized


def resolve_content(
    file_path: str | None = None,
    owl_content: str | None = None,
) -> str:
    """Return ontology content from either file_path or inline content."""
    if file_path and owl_content:
        raise ValueError("Provide either file_path or owl_content, not both")
    if owl_content:
        return owl_content
    if not file_path:
        raise ValueError("Either file_path or owl_content must be provided")
    container_path = resolve_path(file_path)
    path = Path(container_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path} (resolved to {container_path})")
    return path.read_text(encoding="utf-8")


def resolve_folder(folder_path: str) -> Path:
    """Map a host OS folder path to the container-internal path and validate it exists."""
    container_path = Path(resolve_path(folder_path))
    if not container_path.is_dir():
        raise FileNotFoundError(f"Folder not found: {folder_path} (resolved to {container_path})")
    return container_path
