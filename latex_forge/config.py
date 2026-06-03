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


def get_profile() -> dict:
    raw = load_config().get("profile", {})
    return raw if isinstance(raw, dict) else {}


def save_profile(profile: dict) -> None:
    existing_content = _CONFIG_PATH.read_text(encoding="utf-8") if _CONFIG_PATH.exists() else ""

    # Rebuild file without the existing [profile] section
    lines: list[str] = []
    in_profile = False
    for line in existing_content.splitlines():
        if line.strip() == "[profile]":
            in_profile = True
            continue
        if in_profile:
            if line.strip().startswith("["):
                in_profile = False
                lines.append(line)
            # else: skip profile lines
        else:
            lines.append(line)

    # Strip trailing blank lines
    while lines and not lines[-1].strip():
        lines.pop()

    # Append new [profile] section
    if lines:
        lines.append("")
    lines.append("[profile]")
    for key in ("name", "university", "program", "github"):
        value = profile.get(key, "")
        if value:
            lines.append(f'{key} = "{value}"')

    _CONFIG_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
