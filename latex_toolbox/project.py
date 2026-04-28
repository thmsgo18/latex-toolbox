from __future__ import annotations

import shutil
from pathlib import Path


LATEX_BUILD_SUFFIXES = {
    ".aux",
    ".bbl",
    ".bcf",
    ".blg",
    ".fdb_latexmk",
    ".fls",
    ".log",
    ".out",
    ".run.xml",
    ".synctex.gz",
    ".toc",
}

IGNORED_NAMES = {
    ".DS_Store",
}


def toolbox_root() -> Path:
    return Path(__file__).resolve().parent.parent


def templates_dir() -> Path:
    return toolbox_root() / "templates"


def styles_dir() -> Path:
    return toolbox_root() / "styles" / "packages"


def logos_dir() -> Path:
    return toolbox_root() / "assets" / "logos"


def available_templates() -> list[str]:
    return sorted(path.name for path in templates_dir().iterdir() if path.is_dir())


def should_ignore(path: Path) -> bool:
    if path.name in IGNORED_NAMES:
        return True
    return any(path.name.endswith(suffix) for suffix in LATEX_BUILD_SUFFIXES)


def copy_tree(source: Path, destination: Path) -> None:
    for source_path in source.rglob("*"):
        if should_ignore(source_path):
            continue

        relative_path = source_path.relative_to(source)
        destination_path = destination / relative_path

        if source_path.is_dir():
            destination_path.mkdir(parents=True, exist_ok=True)
            continue

        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, destination_path)


def patch_local_style(style_path: Path) -> None:
    if not style_path.exists():
        return

    original = "{{../../assets/images/common/}}{{../../assets/logos/}}"
    replacement = "{{assets/images/common/}}{{assets/logos/}}"
    content = style_path.read_text(encoding="utf-8")
    style_path.write_text(content.replace(original, replacement), encoding="utf-8")


def create_project(name: str, template: str) -> tuple[Path, Path]:
    source_dir = templates_dir() / template
    if not source_dir.is_dir():
        available = ", ".join(available_templates())
        raise ValueError(f"Template inconnu: {template}. Disponibles: {available}")

    base_dir = Path.cwd().resolve()
    target_dir = base_dir / name
    main_tex_file = target_dir / f"{name}.tex"
    local_style_dir = target_dir / "styles" / "packages"

    if target_dir.exists():
        raise FileExistsError(f"Le dossier existe deja: {target_dir}")

    base_dir.mkdir(parents=True, exist_ok=True)
    target_dir.mkdir(parents=True, exist_ok=False)
    copy_tree(source_dir, target_dir)

    copied_main = target_dir / "main.tex"
    if copied_main.exists():
        copied_main.rename(main_tex_file)

    local_style_dir.mkdir(parents=True, exist_ok=True)
    for style_path in sorted(styles_dir().glob("*.sty")):
        shutil.copy2(style_path, local_style_dir / style_path.name)

    (target_dir / "assets" / "images" / "common").mkdir(parents=True, exist_ok=True)
    (target_dir / "assets" / "logos").mkdir(parents=True, exist_ok=True)
    patch_local_style(local_style_dir / "university-project-report.sty")

    for logo_path in sorted(logos_dir().iterdir()):
        if should_ignore(logo_path):
            continue
        destination = target_dir / "assets" / "logos" / logo_path.name
        if logo_path.is_dir():
            shutil.copytree(logo_path, destination)
        else:
            shutil.copy2(logo_path, destination)

    (target_dir / "assets" / "images" / "common" / ".gitkeep").touch(exist_ok=True)
    (target_dir / "assets" / "logos" / ".gitkeep").touch(exist_ok=True)
    return target_dir, main_tex_file
