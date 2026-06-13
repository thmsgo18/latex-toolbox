"""Export a project as a clean archive (sources + PDF) for submission."""
from __future__ import annotations

import zipfile
from pathlib import Path

from .build import _find_main_tex

# Directories that belong to latex-forge tooling or version control rather
# than the document itself — never included in the export.
EXCLUDED_DIRS = {"build", ".vscode", ".git", "scripts", "__pycache__"}
# Individual files that are useful for editing the project but meaningless
# (or confusing) to a reviewer receiving a standalone source archive.
EXCLUDED_FILES = {".DS_Store", ".gitignore", "AGENTS.md", "GETTING_STARTED.md", "latexforge.toml"}
# Auxiliary files produced by LaTeX engines, BibTeX/biber, and latexmk during
# compilation. These are regenerated from the sources, so they're dropped —
# except for the .bbl, which is re-added separately (see export_project).
EXCLUDED_SUFFIXES = (
    ".aux", ".acn", ".acr", ".alg", ".bcf", ".blg", ".dvi",
    ".fdb_latexmk", ".fls", ".glg", ".glo", ".gls", ".idx", ".ilg",
    ".ind", ".ist", ".lof", ".log", ".lot", ".nav", ".nlo", ".out",
    ".ps", ".run.xml", ".snm", ".synctex.gz", ".toc", ".vrb", ".xdv",
)


def _should_include(path: Path, project_dir: Path) -> bool:
    """Decide whether a file belongs in the export archive.

    Excludes anything under a tooling/VCS directory (``EXCLUDED_DIRS``),
    known non-source files (``EXCLUDED_FILES``), and LaTeX build artifacts
    (``EXCLUDED_SUFFIXES``).
    """
    relative_parts = path.relative_to(project_dir).parts
    if any(part in EXCLUDED_DIRS for part in relative_parts):
        return False
    if path.name in EXCLUDED_FILES:
        return False
    if path.name.endswith(EXCLUDED_SUFFIXES):
        return False
    return True


def export_project(project_dir: Path | None = None, output: Path | None = None) -> Path:
    """Bundle the project's sources (and compiled PDF, if any) into a ZIP archive.

    Drops latex-forge tooling files (build/, .vscode/, scripts/, AGENTS.md, ...)
    and LaTeX build artifacts, but keeps a precompiled .bbl next to the sources
    so the bibliography survives on platforms that don't run BibTeX (e.g. arXiv).
    Returns the path to the created archive.
    """
    directory = (project_dir or Path.cwd()).resolve()
    if not directory.is_dir():
        raise FileNotFoundError(f"Project directory not found: {directory}")

    main_tex = _find_main_tex(directory)
    archive_path = (output or directory.parent / f"{directory.name}-export.zip").resolve()

    build_dir = directory / "build"
    pdf_path = build_dir / f"{main_tex.stem}.pdf"
    bbl_path = build_dir / f"{main_tex.stem}.bbl"

    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(directory.rglob("*")):
            if path.is_dir() or not _should_include(path, directory):
                continue
            archive.write(path, path.relative_to(directory))

        if pdf_path.exists():
            archive.write(pdf_path, pdf_path.name)
        if bbl_path.exists():
            archive.write(bbl_path, bbl_path.name)

    return archive_path
