"""Tests for latex_forge.export (latex-forge export)."""
from __future__ import annotations

import zipfile
from pathlib import Path

import pytest

from latex_forge.export import export_project


@pytest.fixture()
def project(tmp_path) -> Path:
    """A minimal generated project with build artifacts and tooling files."""
    proj = tmp_path / "my-report"
    proj.mkdir()
    (proj / "my-report.tex").write_text("\\documentclass{article}", encoding="utf-8")
    (proj / "references.bib").write_text("@article{a, title={A}}", encoding="utf-8")
    (proj / ".gitignore").write_text("build/\n", encoding="utf-8")
    (proj / "AGENTS.md").write_text("agent notes", encoding="utf-8")
    (proj / "GETTING_STARTED.md").write_text("getting started", encoding="utf-8")
    (proj / "latexforge.toml").write_text("engine = \"lualatex\"", encoding="utf-8")

    sections = proj / "sections"
    sections.mkdir()
    (sections / "intro.tex").write_text("\\section{Intro}", encoding="utf-8")

    vscode = proj / ".vscode"
    vscode.mkdir()
    (vscode / "settings.json").write_text("{}", encoding="utf-8")

    scripts = proj / "scripts"
    scripts.mkdir()
    (scripts / "setup.py").write_text("print('setup')", encoding="utf-8")

    git = proj / ".git"
    git.mkdir()
    (git / "config").write_text("", encoding="utf-8")

    build_dir = proj / "build"
    build_dir.mkdir()
    (build_dir / "my-report.pdf").write_bytes(b"%PDF-1.4 fake")
    (build_dir / "my-report.bbl").write_text("\\bibitem{a} A", encoding="utf-8")
    (build_dir / "my-report.aux").write_text("aux", encoding="utf-8")
    (build_dir / "my-report.log").write_text("log", encoding="utf-8")

    (proj / "my-report.aux").write_text("aux", encoding="utf-8")
    (proj / ".DS_Store").write_text("", encoding="utf-8")

    return proj


def test_export_creates_zip_next_to_project(project):
    archive_path = export_project(project)
    assert archive_path == project.parent / "my-report-export.zip"
    assert archive_path.exists()


def test_export_includes_sources_and_pdf(project):
    archive_path = export_project(project)
    with zipfile.ZipFile(archive_path) as archive:
        names = set(archive.namelist())

    assert "my-report.tex" in names
    assert "references.bib" in names
    assert "sections/intro.tex" in names
    assert "my-report.pdf" in names
    assert "my-report.bbl" in names


def test_export_excludes_tooling_and_artifacts(project):
    archive_path = export_project(project)
    with zipfile.ZipFile(archive_path) as archive:
        names = set(archive.namelist())

    assert not any(name.startswith("build/") for name in names)
    assert not any(name.startswith(".vscode/") for name in names)
    assert not any(name.startswith(".git/") for name in names)
    assert not any(name.startswith("scripts/") for name in names)
    assert "AGENTS.md" not in names
    assert "GETTING_STARTED.md" not in names
    assert "latexforge.toml" not in names
    assert ".gitignore" not in names
    assert ".DS_Store" not in names
    assert "my-report.aux" not in names


def test_export_custom_output_path(project, tmp_path):
    output = tmp_path / "custom" / "archive.zip"
    archive_path = export_project(project, output=output)
    assert archive_path == output
    assert output.exists()


def test_export_without_pdf(project):
    (project / "build" / "my-report.pdf").unlink()
    (project / "build" / "my-report.bbl").unlink()

    archive_path = export_project(project)
    with zipfile.ZipFile(archive_path) as archive:
        names = set(archive.namelist())

    assert "my-report.pdf" not in names
    assert "my-report.bbl" not in names
    assert "my-report.tex" in names


def test_export_missing_directory():
    with pytest.raises(FileNotFoundError):
        export_project(Path("/nonexistent/nowhere"))


def test_export_no_main_tex(tmp_path):
    proj = tmp_path / "empty"
    proj.mkdir()
    with pytest.raises(FileNotFoundError):
        export_project(proj)
