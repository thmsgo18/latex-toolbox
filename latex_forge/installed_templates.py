"""Persistence layer for user-installed template metadata.

Stores name, install_url, installed_version, and installed_at for each
template installed by the user.  The data lives in
``~/.latex-forge/installed_templates.json`` as a dict keyed by template name.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


# ── Path ──────────────────────────────────────────────────────────────────


def metadata_path() -> Path:
    return Path.home() / ".latex-forge" / "installed_templates.json"


# ── Load / Save ───────────────────────────────────────────────────────────


def load_all() -> dict[str, dict]:
    """Return a dict of {template_name: metadata_dict}."""
    p = metadata_path()
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _save_all(data: dict[str, dict]) -> None:
    p = metadata_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


# ── Per-template operations ───────────────────────────────────────────────


def get(name: str) -> dict | None:
    """Return metadata for *name*, or None if not tracked."""
    return load_all().get(name)


def record(
    name: str,
    install_url: str | None,
    version: str | None,
) -> None:
    """Persist (or overwrite) metadata for *name*."""
    data = load_all()
    data[name] = {
        "name": name,
        "install_url": install_url,
        "installed_version": version,
        "installed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
    }
    _save_all(data)


def remove(name: str) -> None:
    """Delete metadata for *name* (no-op if not present)."""
    data = load_all()
    if name in data:
        data.pop(name)
        _save_all(data)
