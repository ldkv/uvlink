from pathlib import Path
import hashlib
import os


def hash_path(path: str | Path, length: int = 12) -> str:
    """Generate a deterministic short hash for a filesystem path.

    Args:
        path: Filesystem path to hash; may be relative.
        length: Number of leading hexadecimal characters to
            return from the SHA-256 digest. Defaults to 12.

    Returns:
        str: Prefix of the SHA-256 hash for the resolved absolute path.
    """
    abs_path = Path(path).resolve().as_posix()
    abs_path_hash = hashlib.sha256(abs_path.encode("utf-8")).hexdigest()
    return abs_path_hash[:length]


def get_uvlink_dir(*subpaths: str | Path) -> Path:
    """Return the uvlink data directory, optionally nested under subpaths.

    Args:
        *subpaths: Optional relative paths appended under the uvlink data root.

    Returns:
        Path: Absolute path to the uvlink data directory or provided subpath.
    """
    base = Path(os.environ.get("XDG_DATA_HOME", "~/.local/share")).expanduser()
    root = base / "uvlink"
    for sp in subpaths:
        root /= Path(sp)
    return root


def get_project_name(path: str | Path | None = None) -> str:
    """Return the final directory name for the given project path.

    Args:
        path: Optional filesystem path to inspect. Defaults to the current
            working directory when omitted.

    Returns:
        str: Basename of the provided or current project path.
    """
    p = Path(path or Path.cwd()).expanduser()
    return p.name


def get_project_cache_dir(
    path: str | Path | None = None, venv_type: str = "venv"
) -> Path:
    """Return the cache directory path for the project's virtual environment.

    Args:
        path: Optional project directory; defaults to the current working
            directory when omitted.
        venv_type: Identifier for the virtual environment flavor. Only
            "venv" is currently supported.

    Returns:
        Path: Location under the uvlink cache tree scoped by project name and
            hashed path.

    Raises:
        NotImplementedError: If an unsupported ``venv_type`` is provided.
    """
    project_dir = Path(path or Path.cwd())
    project_name = get_project_name(project_dir)
    project_hash = hash_path(project_dir)
    # TODO: use Enum for venv_type
    if venv_type == "venv":
        cache_dir = get_uvlink_dir("cache", "venv") / f"{project_name}-{project_hash}"
    else:
        raise NotImplementedError(f"venv_type = {venv_type} not supported (yet)")
    return cache_dir
