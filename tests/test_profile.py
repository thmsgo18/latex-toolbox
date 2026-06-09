"""Tests for the profile module: load/save/clear and project application."""
from __future__ import annotations

from pathlib import Path

import pytest

from latex_forge.profile import (
    apply_profile_to_project,
    clear_profile,
    load_profile,
    save_profile,
)


# ── Fixtures ──────────────────────────────────────────────────────────────


@pytest.fixture(autouse=True)
def isolated_profile(tmp_path, monkeypatch):
    """Redirect the profile file to a temp location for every test."""
    import latex_forge.profile as prof

    fake_path = tmp_path / ".latex-forge" / "profile.toml"
    monkeypatch.setattr(prof, "profile_path", lambda: fake_path)
    yield fake_path


@pytest.fixture()
def full_profile() -> dict[str, str]:
    return {
        "first_name": "Thomas",
        "last_name": "Gourmelen",
        "email": "thomas@example.com",
        "phone": "+33 6.00.00.00.00",
        "website": "thomasg.dev",
        "github": "thmsgo18",
        "linkedin": "thomas-gourmelen",
        "university": "Université Paris Cité",
        "faculty": "UFR Informatique",
        "program": "Master Informatique",
        "supervisor": "",
        "company": "",
        "department": "",
        "job_title": "",
    }


# ── save / load / clear ───────────────────────────────────────────────────


def test_load_returns_empty_when_no_file():
    assert load_profile() == {}


def test_save_and_load_round_trip(full_profile):
    save_profile(full_profile)
    loaded = load_profile()
    for key, value in full_profile.items():
        assert loaded.get(key) == value


def test_save_creates_parent_directory(isolated_profile):
    save_profile({"first_name": "Alice"})
    assert isolated_profile.exists()


def test_clear_removes_file(full_profile):
    save_profile(full_profile)
    clear_profile()
    assert not load_profile()


def test_clear_is_noop_when_no_file():
    clear_profile()  # should not raise


# ── apply to blank template ───────────────────────────────────────────────


@pytest.fixture()
def blank_project(tmp_path) -> Path:
    (tmp_path / "frontmatter").mkdir()
    (tmp_path / "frontmatter" / "metadata.tex").write_text(
        "\\title{Document Title}\n\\author{Author Name}\n\\date{\\today}\n"
    )
    return tmp_path


def test_apply_blank_substitutes_author(blank_project, full_profile):
    apply_profile_to_project(blank_project, "blank", full_profile)
    content = (blank_project / "frontmatter" / "metadata.tex").read_text()
    assert "Thomas Gourmelen" in content
    assert "Author Name" not in content


def test_apply_blank_preserves_title(blank_project, full_profile):
    apply_profile_to_project(blank_project, "blank", full_profile)
    content = (blank_project / "frontmatter" / "metadata.tex").read_text()
    assert "Document Title" in content


def test_apply_blank_empty_profile_is_noop(blank_project):
    apply_profile_to_project(blank_project, "blank", {})
    content = (blank_project / "frontmatter" / "metadata.tex").read_text()
    assert "Author Name" in content


# ── apply to cv-en template ───────────────────────────────────────────────


@pytest.fixture()
def cv_en_project(tmp_path) -> Path:
    (tmp_path / "sections").mkdir()
    (tmp_path / "sections" / "heading.tex").write_text(
        "\\textbf{\\Huge First LAST} \\\\\n"
        "\\faPhone* \\texttt{+1 000.000.0000}\n"
        "\\faEnvelope \\texttt{email@example.com}\n"
        "\\href{https://github.com/username}{\\texttt{username}}\n"
        "\\href{https://www.linkedin.com/in/first-last/}{\\texttt{first-last}}\n"
    )
    return tmp_path


def test_apply_cv_en_name(cv_en_project, full_profile):
    apply_profile_to_project(cv_en_project, "cv-en", full_profile)
    content = (cv_en_project / "sections" / "heading.tex").read_text()
    assert "Thomas Gourmelen" in content
    assert "First LAST" not in content


def test_apply_cv_en_email(cv_en_project, full_profile):
    apply_profile_to_project(cv_en_project, "cv-en", full_profile)
    content = (cv_en_project / "sections" / "heading.tex").read_text()
    assert "thomas@example.com" in content
    assert "email@example.com" not in content


def test_apply_cv_en_github(cv_en_project, full_profile):
    apply_profile_to_project(cv_en_project, "cv-en", full_profile)
    content = (cv_en_project / "sections" / "heading.tex").read_text()
    assert "thmsgo18" in content
    assert "username" not in content


def test_apply_cv_en_linkedin(cv_en_project, full_profile):
    apply_profile_to_project(cv_en_project, "cv-en", full_profile)
    content = (cv_en_project / "sections" / "heading.tex").read_text()
    assert "thomas-gourmelen" in content
    assert "first-last" not in content


# ── apply to cv-fr template ───────────────────────────────────────────────


@pytest.fixture()
def cv_fr_project(tmp_path) -> Path:
    (tmp_path / "sections").mkdir()
    (tmp_path / "sections" / "en-tete.tex").write_text(
        "\\textbf{\\Huge Prénom NOM} \\\\\n"
        "\\faPhone* \\texttt{+33 6.00.00.00.00}\n"
        "\\faEnvelope \\texttt{email@example.com}\n"
        "\\href{https://github.com/username}{\\texttt{username}}\n"
        "\\href{https://www.linkedin.com/in/prenom-nom/}{\\texttt{prenom-nom}}\n"
    )
    return tmp_path


def test_apply_cv_fr_name(cv_fr_project, full_profile):
    apply_profile_to_project(cv_fr_project, "cv-fr", full_profile)
    content = (cv_fr_project / "sections" / "en-tete.tex").read_text()
    assert "Thomas Gourmelen" in content
    assert "Prénom NOM" not in content


def test_apply_cv_fr_linkedin(cv_fr_project, full_profile):
    apply_profile_to_project(cv_fr_project, "cv-fr", full_profile)
    content = (cv_fr_project / "sections" / "en-tete.tex").read_text()
    assert "thomas-gourmelen" in content
    assert "prenom-nom" not in content


# ── apply to report templates ─────────────────────────────────────────────


@pytest.fixture()
def report_en_project(tmp_path) -> Path:
    (tmp_path / "frontmatter").mkdir()
    (tmp_path / "frontmatter" / "metadata.tex").write_text(
        "\\newcommand{\\universityname}{Universite Paris Cite}\n"
        "\\newcommand{\\facultyname}{Master's Degree -- Computer Science}\n"
        "\\addauthor{LASTNAME Firstname}{}\n"
    )
    return tmp_path


@pytest.fixture()
def report_fr_project(tmp_path) -> Path:
    (tmp_path / "frontmatter").mkdir()
    (tmp_path / "frontmatter" / "metadata.tex").write_text(
        "\\newcommand{\\universityname}{Universite Paris Cite}\n"
        "\\newcommand{\\facultyname}{Master Informatique}\n"
        "\\addauthor{NOM Prenom}{}\n"
    )
    return tmp_path


def test_apply_report_en_university(report_en_project, full_profile):
    apply_profile_to_project(report_en_project, "project-report-en", full_profile)
    content = (report_en_project / "frontmatter" / "metadata.tex").read_text()
    assert "Université Paris Cité" in content
    assert "Universite Paris Cite" not in content


def test_apply_report_en_program(report_en_project, full_profile):
    apply_profile_to_project(report_en_project, "project-report-en", full_profile)
    content = (report_en_project / "frontmatter" / "metadata.tex").read_text()
    assert "Master Informatique" in content


def test_apply_report_en_author(report_en_project, full_profile):
    apply_profile_to_project(report_en_project, "project-report-en", full_profile)
    content = (report_en_project / "frontmatter" / "metadata.tex").read_text()
    assert "Gourmelen Thomas" in content
    assert "LASTNAME Firstname" not in content


def test_apply_report_fr_author(report_fr_project, full_profile):
    apply_profile_to_project(report_fr_project, "project-report-fr", full_profile)
    content = (report_fr_project / "frontmatter" / "metadata.tex").read_text()
    assert "Gourmelen Thomas" in content
    assert "NOM Prenom" not in content


# ── partial profile ───────────────────────────────────────────────────────


def test_partial_profile_only_substitutes_set_fields(blank_project):
    partial = {"first_name": "Alice", "last_name": "Smith"}
    apply_profile_to_project(blank_project, "blank", partial)
    content = (blank_project / "frontmatter" / "metadata.tex").read_text()
    assert "Alice Smith" in content


def test_missing_name_skips_author(blank_project):
    apply_profile_to_project(blank_project, "blank", {"email": "a@b.com"})
    content = (blank_project / "frontmatter" / "metadata.tex").read_text()
    assert "Author Name" in content  # unchanged


# ── unknown / external template ───────────────────────────────────────────


def test_unknown_template_is_noop(tmp_path, full_profile):
    # No files created — should not raise
    apply_profile_to_project(tmp_path, "some-gallery-template", full_profile)


# ── cv gallery format (frontmatter/metadata.tex with \cvname) ────────────


@pytest.fixture()
def cv_en_gallery_project(tmp_path) -> Path:
    (tmp_path / "frontmatter").mkdir()
    (tmp_path / "frontmatter" / "metadata.tex").write_text(
        "\\newcommand{\\cvname}{First LAST}\n"
        "\\newcommand{\\cvphone}{+1 000.000.0000}\n"
        "\\newcommand{\\cvemail}{email@example.com}\n"
        "\\newcommand{\\cvgithub}{username}\n"
        "\\newcommand{\\cvlinkedin}{first-last}\n"
    )
    return tmp_path


def test_apply_cv_gallery_format(cv_en_gallery_project, full_profile):
    apply_profile_to_project(cv_en_gallery_project, "cv-en", full_profile)
    content = (cv_en_gallery_project / "frontmatter" / "metadata.tex").read_text()
    assert "Thomas Gourmelen" in content
    assert "thomas@example.com" in content
    assert "thmsgo18" in content
    assert "thomas-gourmelen" in content
    assert "First LAST" not in content
