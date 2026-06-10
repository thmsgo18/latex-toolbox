"""Tests for latex_forge.build (latex-forge build / watch)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from latex_forge.build import (
    _detect_latexmk_flag,
    _find_main_tex,
    _find_missing_files,
    _install_missing_packages,
    _tlmgr_package_for_file,
    build_command,
    run_build,
)


# ── Fixtures ──────────────────────────────────────────────────────────────


@pytest.fixture()
def project(tmp_path) -> Path:
    """A minimal generated project: <name>.tex + .vscode/settings.json."""
    proj = tmp_path / "my-report"
    proj.mkdir()
    (proj / "my-report.tex").write_text("\\documentclass{article}", encoding="utf-8")
    vscode = proj / ".vscode"
    vscode.mkdir()
    (vscode / "settings.json").write_text(
        json.dumps({
            "latex-workshop.latex.tools": [
                {
                    "name": "pdflatexmk",
                    "command": "latexmk",
                    "args": [
                        "-synctex=1",
                        "-interaction=nonstopmode",
                        "-file-line-error",
                        "-pdf",
                        "-outdir=%OUTDIR%",
                        "%DOC%",
                    ],
                }
            ]
        }),
        encoding="utf-8",
    )
    return proj


# ── Engine detection ──────────────────────────────────────────────────────


def test_detect_flag_from_settings(project):
    assert _detect_latexmk_flag(project) == "-pdf"


def test_detect_flag_defaults_to_lualatex(tmp_path):
    assert _detect_latexmk_flag(tmp_path) == "-lualatex"


def test_detect_flag_tolerates_broken_settings(tmp_path):
    vscode = tmp_path / ".vscode"
    vscode.mkdir()
    (vscode / "settings.json").write_text("{not json", encoding="utf-8")
    assert _detect_latexmk_flag(tmp_path) == "-lualatex"


# ── Main file resolution ──────────────────────────────────────────────────


def test_find_main_tex_by_folder_name(project):
    assert _find_main_tex(project).name == "my-report.tex"


def test_find_main_tex_single_file(tmp_path):
    (tmp_path / "whatever.tex").touch()
    assert _find_main_tex(tmp_path).name == "whatever.tex"


def test_find_main_tex_none_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        _find_main_tex(tmp_path)


def test_find_main_tex_ambiguous_raises(tmp_path):
    (tmp_path / "a.tex").touch()
    (tmp_path / "b.tex").touch()
    with pytest.raises(ValueError):
        _find_main_tex(tmp_path)


# ── Command construction ──────────────────────────────────────────────────


def test_build_command(project):
    cmd = build_command(project)
    assert cmd[0] == "latexmk"
    assert "-pdf" in cmd
    assert "-outdir=build" in cmd
    assert "-quiet" in cmd
    assert cmd[-1] == "my-report.tex"
    assert "-pvc" not in cmd


def test_build_command_watch_adds_pvc(project):
    assert "-pvc" in build_command(project, watch=True)


def test_build_command_verbose_drops_quiet(project):
    assert "-quiet" not in build_command(project, verbose=True)


# ── run_build behaviour ───────────────────────────────────────────────────


def test_run_build_missing_latexmk(project, monkeypatch, capsys):
    monkeypatch.setattr("latex_forge.build.shutil.which", lambda _: None)
    assert run_build(project) == 1
    assert "latex-forge setup" in capsys.readouterr().out


def test_run_build_invokes_latexmk(project, monkeypatch):
    monkeypatch.setattr("latex_forge.build.shutil.which", lambda _: "/usr/bin/latexmk")
    calls: dict = {}

    def fake_run(command, cwd, check):
        calls["command"] = command
        calls["cwd"] = cwd

        class R:
            returncode = 0

        return R()

    monkeypatch.setattr("latex_forge.build.subprocess.run", fake_run)
    assert run_build(project) == 0
    assert calls["command"][-1] == "my-report.tex"
    assert calls["cwd"] == project.resolve()


def test_run_build_clean_removes_build_dir(project, monkeypatch):
    build_dir = project / "build"
    build_dir.mkdir()
    (build_dir / "stale.aux").touch()

    monkeypatch.setattr("latex_forge.build.shutil.which", lambda _: "/usr/bin/latexmk")

    def fake_run(command, cwd, check):
        class R:
            returncode = 0

        return R()

    monkeypatch.setattr("latex_forge.build.subprocess.run", fake_run)
    run_build(project, clean=True)
    assert not build_dir.exists()


def test_run_build_missing_directory():
    with pytest.raises(FileNotFoundError):
        run_build(Path("/nonexistent/nowhere"))


def test_run_build_propagates_exit_code(project, monkeypatch):
    monkeypatch.setattr("latex_forge.build.shutil.which", lambda _: "/usr/bin/latexmk")

    def fake_run(command, cwd, check):
        class R:
            returncode = 12

        return R()

    monkeypatch.setattr("latex_forge.build.subprocess.run", fake_run)
    assert run_build(project) == 12


# ── Missing package detection & auto-install ──────────────────────────────


def test_find_missing_files_parses_log(tmp_path):
    log = tmp_path / "my-report.log"
    log.write_text(
        "! LaTeX Error: File `tikz.sty' not found.\n"
        "Some other line\n"
        "! LaTeX Error: File `tikz.sty' not found.\n",
        encoding="utf-8",
    )
    assert _find_missing_files(log) == ["tikz.sty"]


def test_find_missing_files_no_log(tmp_path):
    assert _find_missing_files(tmp_path / "nope.log") == []


def test_tlmgr_package_for_file(monkeypatch):
    def fake_run(command, capture_output, text, check):
        class R:
            returncode = 0
            stdout = "tikz.sty:\n\tpgf:\n\t\ttexmf-dist/tex/generic/pgf/frontendlayer/tikz/tikz.sty\n"

        return R()

    monkeypatch.setattr("latex_forge.build.subprocess.run", fake_run)
    assert _tlmgr_package_for_file("tikz.sty") == "pgf"


def test_tlmgr_package_for_file_not_found(monkeypatch):
    def fake_run(command, capture_output, text, check):
        class R:
            returncode = 1
            stdout = ""

        return R()

    monkeypatch.setattr("latex_forge.build.subprocess.run", fake_run)
    assert _tlmgr_package_for_file("doesnotexist.sty") is None


def test_install_missing_packages_no_tlmgr(monkeypatch):
    monkeypatch.setattr("latex_forge.build.shutil.which", lambda _: None)
    assert _install_missing_packages(["tikz.sty"]) == []


def test_install_missing_packages_installs(monkeypatch):
    monkeypatch.setattr("latex_forge.build.shutil.which", lambda _: "/usr/bin/tlmgr")

    def fake_run(command, capture_output, text, check):
        class R:
            returncode = 0
            stdout = ""

        if command[1] == "search":
            R.stdout = "tikz.sty:\n\tpgf:\n\t\tsome/path/tikz.sty\n"
        return R()

    monkeypatch.setattr("latex_forge.build.subprocess.run", fake_run)
    assert _install_missing_packages(["tikz.sty"]) == ["pgf"]


def test_run_build_retries_after_installing_missing_package(project, monkeypatch, capsys):
    monkeypatch.setattr("latex_forge.build.shutil.which", lambda name: f"/usr/bin/{name}")

    log_path = project / "build" / "my-report.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("! LaTeX Error: File `tikz.sty' not found.\n", encoding="utf-8")

    calls = {"latexmk": 0}

    def fake_run(command, cwd=None, check=False, capture_output=False, text=False):
        if command[0] == "latexmk":
            calls["latexmk"] += 1

            class R:
                returncode = 1

            return R()
        if command[:2] == ["tlmgr", "search"]:
            class R:
                returncode = 0
                stdout = "tikz.sty:\n\tpgf:\n\t\tsome/path/tikz.sty\n"

            return R()
        if command[:2] == ["tlmgr", "install"]:
            class R:
                returncode = 0
                stdout = ""

            return R()
        raise AssertionError(f"Unexpected command: {command}")

    monkeypatch.setattr("latex_forge.build.subprocess.run", fake_run)
    result = run_build(project)

    assert result == 1
    assert calls["latexmk"] == 2
    out = capsys.readouterr().out
    assert "Missing package files: tikz.sty" in out
    assert "Installed: pgf" in out


def test_run_build_no_retry_without_missing_packages(project, monkeypatch, capsys):
    monkeypatch.setattr("latex_forge.build.shutil.which", lambda name: f"/usr/bin/{name}")

    calls = {"latexmk": 0}

    def fake_run(command, cwd=None, check=False, capture_output=False, text=False):
        calls["latexmk"] += 1

        class R:
            returncode = 1

        return R()

    monkeypatch.setattr("latex_forge.build.subprocess.run", fake_run)
    result = run_build(project)

    assert result == 1
    assert calls["latexmk"] == 1
