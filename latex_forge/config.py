from __future__ import annotations

import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib  # type: ignore[no-redef]
    except ImportError:
        tomllib = None  # type: ignore[assignment]

_CONFIG_PATH = Path.home() / ".latex-forge.toml"


def load_config() -> dict:
    if tomllib is None or not _CONFIG_PATH.exists():
        return {}
    try:
        with open(_CONFIG_PATH, "rb") as f:
            return tomllib.load(f)
    except Exception:
        return {}


def get_default_template() -> str | None:
    value = load_config().get("default_template")
    return value if isinstance(value, str) and value else None


def get_default_output_dir() -> Path | None:
    value = load_config().get("default_output_dir")
    if not isinstance(value, str) or not value:
        return None
    path = Path(value).expanduser().resolve()
    return path if path.is_dir() else None


