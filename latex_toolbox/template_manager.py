"""Install, remove and list user-installed templates."""
from __future__ import annotations

import shutil
import tempfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path


# ── Public API ────────────────────────────────────────────────────────────


def install_template(source: str, name: str | None = None) -> tuple[str, Path]:
    """Install a template from a GitHub URL, ZIP URL, or local path.

    Returns ``(template_name, installed_path)``.

    Supported sources:
    - ``https://github.com/owner/repo``
    - ``https://github.com/owner/repo/tree/branch/path/to/subdir``
    - Any ``https://`` URL ending in ``.zip``
    - A local directory
    - A local ``.zip`` file
    """
    source = source.strip()

    if "github.com" in source:
        return _install_from_github(source, name)

    if source.startswith(("https://", "http://")) and source.endswith(".zip"):
        return _install_from_zip_url(source, name)

    local = Path(source).expanduser().resolve()
    if local.exists():
        if local.is_dir():
            return _install_from_dir(local, name)
        if local.suffix == ".zip":
            return _install_from_zip_file(local, name)

    raise ValueError(
        f"Cannot install template from: {source!r}\n"
        "Supported sources:\n"
        "  - GitHub URL  : https://github.com/owner/repo\n"
        "  - ZIP URL     : https://example.com/template.zip\n"
        "  - Local dir   : /path/to/template/\n"
        "  - Local ZIP   : /path/to/template.zip"
    )


def remove_template(name: str) -> None:
    """Remove a user-installed template.

    Raises ``ValueError`` if the template is built-in.
    Raises ``FileNotFoundError`` if the template is not installed.
    """
    from .project import templates_dir

    if (templates_dir() / name).is_dir():
        raise ValueError(
            f"'{name}' is a built-in template and cannot be removed.\n"
            "Only user-installed templates can be removed."
        )
    dest = _user_template_path(name)
    if not dest.exists():
        raise FileNotFoundError(f"Installed template not found: {name!r}")
    shutil.rmtree(dest)


def list_user_templates() -> list[str]:
    """Return the names of all user-installed templates."""
    d = _user_templates_dir()
    if not d.exists():
        return []
    return sorted(p.name for p in d.iterdir() if p.is_dir())


# ── Paths ─────────────────────────────────────────────────────────────────


def _user_templates_dir() -> Path:
    return Path.home() / ".latex-toolbox" / "templates"


def _user_template_path(name: str) -> Path:
    return _user_templates_dir() / name


# ── Download helpers ──────────────────────────────────────────────────────


def _download_url(url: str, dest: Path) -> None:
    print(f"  Downloading {url} …")
    try:
        urllib.request.urlretrieve(url, dest)
    except urllib.error.HTTPError as exc:
        raise ValueError(f"Download failed (HTTP {exc.code}): {url}") from exc
    except urllib.error.URLError as exc:
        raise ValueError(f"Download failed: {exc.reason}") from exc


# ── Install from various sources ──────────────────────────────────────────


def _install_from_github(url: str, name: str | None) -> tuple[str, Path]:
    """Install from a GitHub URL, optionally pointing to a subdirectory."""
    parts = url.rstrip("/").split("/")

    try:
        gh_idx = next(i for i, p in enumerate(parts) if p == "github.com")
        owner = parts[gh_idx + 1]
        repo = parts[gh_idx + 2]
    except (StopIteration, IndexError):
        raise ValueError(f"Invalid GitHub URL: {url!r}")

    subdir: str | None = None
    if "tree" in parts:
        tree_idx = parts.index("tree")
        if len(parts) > tree_idx + 2:
            subdir = "/".join(parts[tree_idx + 2:])

    template_name = name or (subdir.split("/")[-1] if subdir else repo)
    zip_url = f"https://github.com/{owner}/{repo}/archive/HEAD.zip"

    with tempfile.TemporaryDirectory() as tmp:
        zip_path = Path(tmp) / "repo.zip"
        _download_url(zip_url, zip_path)
        return _extract_and_install(
            zip_path,
            extract_to=Path(tmp) / "extracted",
            subdir=subdir,
            name=template_name,
        )


def _install_from_zip_url(url: str, name: str | None) -> tuple[str, Path]:
    template_name = name or Path(url.rstrip("/")).stem
    with tempfile.TemporaryDirectory() as tmp:
        zip_path = Path(tmp) / "template.zip"
        _download_url(zip_url=url, dest=zip_path)
        return _extract_and_install(
            zip_path,
            extract_to=Path(tmp) / "extracted",
            subdir=None,
            name=template_name,
        )


def _install_from_zip_file(zip_path: Path, name: str | None) -> tuple[str, Path]:
    template_name = name or zip_path.stem
    with tempfile.TemporaryDirectory() as tmp:
        return _extract_and_install(
            zip_path,
            extract_to=Path(tmp) / "extracted",
            subdir=None,
            name=template_name,
        )


def _install_from_dir(source: Path, name: str | None) -> tuple[str, Path]:
    template_name = name or source.name
    return _copy_to_user_library(source, template_name)


# ── Core install logic ────────────────────────────────────────────────────


def _extract_and_install(
    zip_path: Path,
    extract_to: Path,
    subdir: str | None,
    name: str,
) -> tuple[str, Path]:
    extract_to.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(extract_to)

    # Case 1: flat ZIP — main.tex sits directly at the extraction root
    if (extract_to / "main.tex").exists():
        source = extract_to
        return _copy_to_user_library(source, name)

    # Case 2: GitHub-style ZIP — files are wrapped inside a top-level directory
    # (e.g. repo-HEAD/ or repo-abc123/)
    top_dirs = [d for d in extract_to.iterdir() if d.is_dir()]
    if not top_dirs:
        raise ValueError("The archive appears to be empty or has no recognizable structure.")
    root = top_dirs[0]

    source = root / subdir if subdir else root

    if not source.exists():
        raise ValueError(
            f"Path {subdir!r} not found inside the archive.\n"
            f"Available entries: {[d.name for d in root.iterdir()]}"
        )

    # If still no main.tex and there is a single sub-directory, descend one level
    if not (source / "main.tex").exists():
        children = [c for c in source.iterdir() if c.is_dir()]
        if len(children) == 1:
            source = children[0]

    return _copy_to_user_library(source, name)


def _copy_to_user_library(source: Path, name: str) -> tuple[str, Path]:
    """Validate and copy a template directory into the user library."""
    if not (source / "main.tex").exists():
        raise ValueError(
            f"No main.tex found in {source}\n"
            "A valid latex-toolbox template must contain a main.tex file."
        )

    dest = _user_template_path(name)
    _user_templates_dir().mkdir(parents=True, exist_ok=True)

    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(source, dest)
    return name, dest
