"""Tests for the fast per-template gallery archive install path."""
from __future__ import annotations

import zipfile
from pathlib import Path

import pytest

import latex_forge.template_manager as tm
from latex_forge.template_manager import (
    _GALLERY_ARCHIVE_BASE,
    _gallery_archive_url,
    install_template,
)


@pytest.fixture(autouse=True)
def isolated_user_dir(tmp_path, monkeypatch):
    import latex_forge.project as proj

    fake_dir = tmp_path / "user_templates"
    fake_meta = tmp_path / "installed_templates.json"

    monkeypatch.setattr(tm, "_user_templates_dir", lambda: fake_dir)
    monkeypatch.setattr(proj, "user_templates_dir", lambda: fake_dir)

    import latex_forge.installed_templates as meta
    monkeypatch.setattr(meta, "metadata_path", lambda: fake_meta)

    # Avoid a real network call in _record_installation's version lookup.
    monkeypatch.setattr(tm, "fetch_gallery_json", lambda *a, **kw: {"templates": []})

    yield fake_dir


GALLERY_URL = (
    "https://github.com/thmsgo18/latex-forge-gallery/tree/main/templates/thesis/clean-thesis"
)


def _write_zip(path: Path, files: dict[str, str]) -> None:
    with zipfile.ZipFile(path, "w") as zf:
        for name, content in files.items():
            zf.writestr(name, content)


# ── _gallery_archive_url ─────────────────────────────────────────────────


def test_gallery_archive_url_matches_template_subdir():
    url = _gallery_archive_url("thmsgo18", "latex-forge-gallery", "templates/thesis/clean-thesis")
    assert url == _GALLERY_ARCHIVE_BASE + "clean-thesis.zip"


def test_gallery_archive_url_ignores_other_repo():
    assert _gallery_archive_url("someone", "their-template", "templates/thesis/clean-thesis") is None


def test_gallery_archive_url_ignores_non_template_subdir():
    assert _gallery_archive_url("thmsgo18", "latex-forge-gallery", "docs") is None
    assert _gallery_archive_url("thmsgo18", "latex-forge-gallery", None) is None


# ── _install_from_github fast path ───────────────────────────────────────


def test_install_from_github_uses_archive_when_available(monkeypatch, isolated_user_dir):
    requested_urls: list[str] = []

    def fake_download(url, dest):
        requested_urls.append(url)
        assert url == _GALLERY_ARCHIVE_BASE + "clean-thesis.zip"
        _write_zip(dest, {"main.tex": "\\documentclass{article}", "sections/intro.tex": "intro"})

    monkeypatch.setattr(tm, "_download_url", fake_download)

    name, path = install_template(GALLERY_URL)

    assert name == "clean-thesis"
    assert (path / "main.tex").exists()
    assert (path / "sections" / "intro.tex").exists()
    assert requested_urls == [_GALLERY_ARCHIVE_BASE + "clean-thesis.zip"]


def test_install_from_github_falls_back_when_archive_missing(monkeypatch, isolated_user_dir):
    requested_urls: list[str] = []

    def fake_download(url, dest):
        requested_urls.append(url)
        if url == _GALLERY_ARCHIVE_BASE + "clean-thesis.zip":
            raise ValueError("Download failed (HTTP 404): " + url)
        # Full-repo GitHub-style ZIP: files wrapped in a top-level directory.
        _write_zip(dest, {
            "latex-forge-gallery-main/templates/thesis/clean-thesis/main.tex": "\\documentclass{article}",
            "latex-forge-gallery-main/templates/thesis/clean-thesis/sections/intro.tex": "intro",
            "latex-forge-gallery-main/README.md": "gallery",
        })

    monkeypatch.setattr(tm, "_download_url", fake_download)

    name, path = install_template(GALLERY_URL)

    assert name == "clean-thesis"
    assert (path / "main.tex").exists()
    assert requested_urls == [
        _GALLERY_ARCHIVE_BASE + "clean-thesis.zip",
        "https://github.com/thmsgo18/latex-forge-gallery/archive/HEAD.zip",
    ]
