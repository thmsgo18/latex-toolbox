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
