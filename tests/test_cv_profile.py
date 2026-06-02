"""Tests for apply_profile_to_cv_heading."""
from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from latex_toolbox.project import apply_profile_to_cv_heading


def _make_heading(tmp_path: Path, content: str) -> Path:
    p = tmp_path / "heading.tex"
    p.write_text(textwrap.dedent(content), encoding="utf-8")
    return p


# ── Name replacement ───────────────────────────────────────────────────────

def test_name_replaced_en(tmp_path):
    heading = _make_heading(tmp_path, r"\textbf{\Huge First LAST}")
    apply_profile_to_cv_heading(heading, {"name": "Thomas Gourmelen"}, "cv-en")
    assert "Thomas Gourmelen" in heading.read_text(encoding="utf-8")
    assert "First LAST" not in heading.read_text(encoding="utf-8")


def test_name_replaced_fr(tmp_path):
    heading = _make_heading(tmp_path, r"\textbf{\Huge Prénom NOM}")
    apply_profile_to_cv_heading(heading, {"name": "Thomas Gourmelen"}, "cv-fr")
    assert "Thomas Gourmelen" in heading.read_text(encoding="utf-8")
    assert "Prénom NOM" not in heading.read_text(encoding="utf-8")


# ── GitHub replacement ─────────────────────────────────────────────────────

def test_github_replaced(tmp_path):
    heading = _make_heading(
        tmp_path,
        r"\href{https://github.com/username}{\texttt{username}}",
    )
    apply_profile_to_cv_heading(heading, {"github": "thmsgo18"}, "cv-en")
    content = heading.read_text(encoding="utf-8")
    assert "thmsgo18" in content
    assert "username" not in content
    assert "https://github.com/thmsgo18" in content


def test_github_and_name_together(tmp_path):
    heading = _make_heading(
        tmp_path,
        "\\textbf{\\Huge First LAST}\n"
        "\\href{https://github.com/username}{\\texttt{username}}",
    )
    apply_profile_to_cv_heading(
        heading, {"name": "Alice Dupont", "github": "alicedupont"}, "cv-en"
    )
    content = heading.read_text(encoding="utf-8")
    assert "Alice Dupont" in content
    assert "alicedupont" in content
    assert "First LAST" not in content
    assert "username" not in content


# ── Edge cases ─────────────────────────────────────────────────────────────

def test_missing_file_is_silent(tmp_path):
    """No exception when heading file does not exist."""
    apply_profile_to_cv_heading(
        tmp_path / "nonexistent.tex", {"name": "Alice"}, "cv-en"
    )


def test_empty_profile_leaves_file_unchanged(tmp_path):
    original = "\\textbf{\\Huge First LAST}\n"
    heading = _make_heading(tmp_path, original)
    apply_profile_to_cv_heading(heading, {}, "cv-en")
    assert heading.read_text(encoding="utf-8") == original


def test_no_name_in_profile_leaves_placeholder(tmp_path):
    heading = _make_heading(tmp_path, "\\textbf{\\Huge First LAST}\n")
    apply_profile_to_cv_heading(heading, {"github": "thmsgo18"}, "cv-en")
    assert "First LAST" in heading.read_text(encoding="utf-8")


def test_no_github_in_profile_leaves_placeholder(tmp_path):
    original = "\\href{https://github.com/username}{\\texttt{username}}\n"
    heading = _make_heading(tmp_path, original)
    apply_profile_to_cv_heading(heading, {"name": "Alice"}, "cv-en")
    assert "username" in heading.read_text(encoding="utf-8")
