from __future__ import annotations

from pathlib import Path

import pytest

from latex_toolbox.project import apply_profile_to_metadata


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_apply_profile_name_en(tmp_path):
    f = tmp_path / "frontmatter" / "metadata.tex"
    _write(f, "\\addauthor{LASTNAME Firstname}{}\n")
    apply_profile_to_metadata(f, {"name": "Dupont Alice"})
    assert "\\addauthor{Dupont Alice}{}" in f.read_text(encoding="utf-8")


def test_apply_profile_name_fr(tmp_path):
    f = tmp_path / "frontmatter" / "metadata.tex"
    _write(f, "\\addauthor{NOM Prenom}{}\n")
    apply_profile_to_metadata(f, {"name": "Dupont Alice"})
    assert "\\addauthor{Dupont Alice}{}" in f.read_text(encoding="utf-8")


def test_apply_profile_name_ter(tmp_path):
    f = tmp_path / "frontmatter" / "metadata.tex"
    _write(f, "\\addauthor{FirstName LASTNAME}{}\n")
    apply_profile_to_metadata(f, {"name": "Alice Dupont"})
    assert "\\addauthor{Alice Dupont}{}" in f.read_text(encoding="utf-8")


def test_apply_profile_github_appended(tmp_path):
    f = tmp_path / "frontmatter" / "metadata.tex"
    _write(f, "\\addauthor{LASTNAME Firstname}{}\n")
    apply_profile_to_metadata(f, {"name": "Dupont Alice", "github": "dupont-alice"})
    assert "\\addauthor{Dupont Alice}{}[dupont-alice]" in f.read_text(encoding="utf-8")


def test_apply_profile_github_only(tmp_path):
    f = tmp_path / "frontmatter" / "metadata.tex"
    _write(f, "\\addauthor{LASTNAME Firstname}{}\n")
    apply_profile_to_metadata(f, {"github": "dupont-alice"})
    assert "[dupont-alice]" in f.read_text(encoding="utf-8")


def test_apply_profile_university(tmp_path):
    f = tmp_path / "frontmatter" / "metadata.tex"
    _write(f, "\\newcommand{\\universityname}{Universite Paris Cite}\n")
    apply_profile_to_metadata(f, {"university": "Université de Bordeaux"})
    assert "Université de Bordeaux" in f.read_text(encoding="utf-8")


def test_apply_profile_program(tmp_path):
    f = tmp_path / "frontmatter" / "metadata.tex"
    _write(f, "\\newcommand{\\facultyname}{Master Informatique}\n")
    apply_profile_to_metadata(f, {"program": "Master IA"})
    assert "Master IA" in f.read_text(encoding="utf-8")


def test_apply_profile_empty_profile_no_change(tmp_path):
    f = tmp_path / "frontmatter" / "metadata.tex"
    original = "\\addauthor{LASTNAME Firstname}{}\n"
    _write(f, original)
    apply_profile_to_metadata(f, {})
    assert f.read_text(encoding="utf-8") == original


def test_apply_profile_missing_file_no_error(tmp_path):
    f = tmp_path / "frontmatter" / "metadata.tex"
    apply_profile_to_metadata(f, {"name": "Alice"})  # should not raise


def test_apply_profile_full(tmp_path):
    f = tmp_path / "frontmatter" / "metadata.tex"
    content = (
        "\\newcommand{\\universityname}{Universite Paris Cite}\n"
        "\\newcommand{\\facultyname}{Master's Degree -- Computer Science}\n"
        "\\addauthor{LASTNAME Firstname}{}\n"
    )
    _write(f, content)
    apply_profile_to_metadata(
        f,
        {
            "name": "Thomas Gourmelen",
            "university": "Université de Bordeaux",
            "program": "Master Informatique",
            "github": "thmsgo18",
        },
    )
    result = f.read_text(encoding="utf-8")
    assert "Université de Bordeaux" in result
    assert "Master Informatique" in result
    assert "\\addauthor{Thomas Gourmelen}{}[thmsgo18]" in result
