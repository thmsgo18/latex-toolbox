from __future__ import annotations

from unittest.mock import patch

from latex_forge.cli import main


def test_version(capsys):
    try:
        main(["--version"])
    except SystemExit as exc:
        assert exc.code == 0
    out = capsys.readouterr().out
    assert "latex-forge" in out


def test_list_templates(capsys):
    result = main(["list-templates"])
    assert result == 0
    out = capsys.readouterr().out
    assert "project-report-en" in out
    assert "research" in out


def test_create_invalid_name(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    with patch("latex_forge.cli.is_first_run", return_value=False):
        result = main(["create", "--name", "bad name", "--template", "project-report-en"])
    assert result == 1
    assert "Invalid project name" in capsys.readouterr().err


def test_create_unknown_template(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    with patch("latex_forge.cli.is_first_run", return_value=False):
        result = main(["create", "--name", "my-project", "--template", "does-not-exist"])
    assert result == 1
    assert "Unknown template" in capsys.readouterr().err


def test_create_success(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    with patch("latex_forge.cli.is_first_run", return_value=False):
        result = main(["create", "--name", "my-project", "--template", "project-report-en"])
    assert result == 0
    assert (tmp_path / "my-project" / "my-project.tex").exists()


def test_export_success(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    with patch("latex_forge.cli.is_first_run", return_value=False):
        main(["create", "--name", "my-project", "--template", "project-report-en"])
    capsys.readouterr()

    result = main(["export", "my-project"])
    assert result == 0
    out = capsys.readouterr().out
    assert "Exported:" in out
    assert "no compiled PDF" in out
    assert (tmp_path / "my-project-export.zip").exists()


def test_export_missing_directory(tmp_path, capsys):
    result = main(["export", str(tmp_path / "does-not-exist")])
    assert result == 1
    assert "not found" in capsys.readouterr().err


def test_create_with_git(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("GIT_AUTHOR_NAME", "Test")
    monkeypatch.setenv("GIT_AUTHOR_EMAIL", "test@example.com")
    monkeypatch.setenv("GIT_COMMITTER_NAME", "Test")
    monkeypatch.setenv("GIT_COMMITTER_EMAIL", "test@example.com")
    with patch("latex_forge.cli.is_first_run", return_value=False):
        result = main(["create", "--name", "my-project", "--template", "project-report-en", "--git"])
    assert result == 0
    assert (tmp_path / "my-project" / ".git").is_dir()
    assert "Initialized a git repository" in capsys.readouterr().out
