from __future__ import annotations

import json
import os
import re
import shutil
from pathlib import Path


_AUTHOR_PLACEHOLDERS = [
    "LASTNAME Firstname",
    "FirstName LASTNAME",
    "NOM Prenom",
]
_UNIVERSITY_PLACEHOLDERS = [
    "Universite Paris Cite",
    "Example University",
]
_PROGRAM_PLACEHOLDERS = [
    "Master Informatique",
    "Master's Degree -- Computer Science",
    "Department of Computer Science",
]

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

LOCAL_STYLE_PATTERN = re.compile(
    r"\\(?:RequirePackage|usepackage)(?:\[[^\]]*\])?\{([^}]*)\}"
)

_FORBIDDEN_NAME_CHARS = re.compile(r'[ /\\:*?"<>|]')


def write_getting_started_guide(target_dir: Path, name: str, template: str) -> None:
    # Template-specific sections
    _BIBLIOGRAPHY = {
        "rapport-ter": """\

### Add a bibliography reference

Add your reference to `bibliography/references.bib`, then cite it in your text:

```latex
This result has been demonstrated in prior work~\\cite{author2024}.
```

The bibliography is printed automatically at the end of the document.
""",
        "research": """\

### Add a bibliography reference

Add your reference to `references/references.bib`, then cite it in your text:

```latex
This result has been demonstrated in prior work~\\cite{author2024}.
```

The bibliography is printed automatically at the end of the document.
""",
    }

    _EXTRA_FOLDERS = {
        "rapport-ter": "| `bibliography/` | BibTeX reference file |\n"
                       "| `appendices/` | Appendices |\n",
        "research": "| `references/` | BibTeX reference file |\n"
                    "| `appendix/` | Appendices and supplementary material |\n",
    }

    bibliography_section = _BIBLIOGRAPHY.get(template, "")
    extra_folders = _EXTRA_FOLDERS.get(template, "")

    content = f"""\
# Getting Started — {name}

## Workflow

**1. Fill in your metadata**

Open `frontmatter/metadata.tex` and set the title, author(s), course, and university.

**2. Write your content**

Add or edit files in `sections/`. To add a new section:
1. Create `sections/my-section.tex`
2. Add `\\input{{sections/my-section.tex}}` to `{name}.tex`

**3. Save to compile**

Save `{name}.tex` in VS Code → LaTeX Workshop compiles automatically → PDF in `build/{name}.pdf`.

---

## Folder structure

| Folder | Purpose |
|---|---|
| `frontmatter/` | Title page data (`metadata.tex`) and table of contents |
| `sections/` | Main content — one `.tex` file per section |
| `backmatter/` | AI statement and end matter |
| `images/` | All images: photos, screenshots, PNG/JPG files |
| `figures/` | TikZ/pgfplots diagrams (LaTeX source figures, not image files) |
| `assets/logos/` | University and project logos |
{extra_folders}\
| `styles/packages/` | Embedded LaTeX styles — do not edit |
| `build/` | Compiled PDF — auto-generated, do not commit |

---

## Common operations

### Add an image

Put your image file in `images/`, then in your `.tex` file:

```latex
\\begin{{figure}}[h]
  \\centering
  \\includegraphics[width=0.8\\linewidth]{{my-image.png}}
  \\caption{{Caption here.}}
  \\label{{fig:my-label}}
\\end{{figure}}
```
{bibliography_section}
### Rename this project

```bash
latex-toolbox rename new-name
```

This renames the folder, the main `.tex` file, and any build artifacts.

---

## If compilation fails

1. **LaTeX not installed** → run `latex-toolbox setup --install-tex`
2. **LaTeX Workshop not installed** → install it from the VS Code extensions panel
3. **Missing package** → `tlmgr install package-name` (TeX Live) or let MiKTeX auto-install
4. **Compilation stuck** → delete the `build/` folder and try again

This project uses **LuaLaTeX**. Verify it is available:

```bash
lualatex --version
```
"""
    (target_dir / "GETTING_STARTED.md").write_text(content, encoding="utf-8")


def apply_profile_to_metadata(metadata_path: Path, profile: dict) -> None:
    if not metadata_path.exists() or not profile:
        return

    content = metadata_path.read_text(encoding="utf-8")

    name = profile.get("name", "")
    university = profile.get("university", "")
    program = profile.get("program", "")
    github = profile.get("github", "")

    if name or github:
        github_suffix = f"[{github}]" if github else ""
        for placeholder in _AUTHOR_PLACEHOLDERS:
            old = f"\\addauthor{{{placeholder}}}{{}}"
            new = f"\\addauthor{{{name or placeholder}}}{{}}{github_suffix}"
            content = content.replace(old, new)

    if university:
        for placeholder in _UNIVERSITY_PLACEHOLDERS:
            content = content.replace(placeholder, university)

    if program:
        for placeholder in _PROGRAM_PLACEHOLDERS:
            content = content.replace(placeholder, program)

    metadata_path.write_text(content, encoding="utf-8")


def validate_name(name: str) -> None:
    if not name:
        raise ValueError("Project name cannot be empty.")
    if _FORBIDDEN_NAME_CHARS.search(name):
        raise ValueError(
            f"Invalid project name: {name!r}. "
            "Avoid spaces and special characters — use hyphens (e.g. my-project)."
        )
    if name.startswith("."):
        raise ValueError(f"Project name cannot start with a dot: {name!r}.")


def package_dir() -> Path:
    return Path(__file__).resolve().parent


def templates_dir() -> Path:
    return package_dir() / "templates"


def styles_dir() -> Path:
    return package_dir() / "styles" / "packages"


def logos_dir() -> Path:
    return package_dir() / "assets" / "logos"


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
    content = style_path.read_text(encoding="utf-8")
    patched = re.sub(r"\.\./\.\./assets/", "assets/", content)
    if patched != content:
        style_path.write_text(patched, encoding="utf-8")


def local_style_dependencies(file_path: Path) -> list[str]:
    content = file_path.read_text(encoding="utf-8")
    dependencies: list[str] = []

    for match in LOCAL_STYLE_PATTERN.finditer(content):
        packages = [item.strip() for item in match.group(1).split(",")]
        for package_name in packages:
            if not package_name.startswith("styles/packages/"):
                continue
            style_name = package_name.removeprefix("styles/packages/")
            if not style_name.endswith(".sty"):
                style_name += ".sty"
            dependencies.append(style_name)

    return dependencies


def required_style_files(source_dir: Path) -> list[Path]:
    main_tex = source_dir / "main.tex"
    if not main_tex.exists():
        return []

    pending = local_style_dependencies(main_tex)
    resolved: set[str] = set()

    while pending:
        style_name = pending.pop()
        if style_name in resolved:
            continue

        style_path = styles_dir() / style_name
        if not style_path.exists():
            continue

        resolved.add(style_name)
        pending.extend(local_style_dependencies(style_path))

    return [styles_dir() / style_name for style_name in sorted(resolved)]


def write_project_vscode_settings(target_dir: Path) -> None:
    vscode_dir = target_dir / ".vscode"
    vscode_dir.mkdir(parents=True, exist_ok=True)

    settings = {
        "[latex]": {"editor.wordWrap": "on"},
        "[tex]": {"editor.wordWrap": "on"},
        "latex-workshop.view.pdf.viewer": "tab",
        "latex-workshop.latex.autoBuild.run": "onSave",
        "latex-workshop.latex.recipe.default": "first",
        "latex-workshop.latex.outDir": "%DIR%/build",
        "latex-workshop.latex.clean.subfolder.enabled": True,
        "latex-workshop.linting.chktex.enabled": False,
        "latex-workshop.linting.lacheck.enabled": False,
        "latex-workshop.latex.tools": [
            {
                "name": "lualatexmk",
                "command": "latexmk",
                "args": [
                    "-synctex=1",
                    "-interaction=nonstopmode",
                    "-file-line-error",
                    "-lualatex",
                    "-outdir=%OUTDIR%",
                    "%DOC%",
                ],
            }
        ],
        "latex-workshop.latex.recipes": [
            {"name": "lualatexmk", "tools": ["lualatexmk"]}
        ],
    }

    settings_path = vscode_dir / "settings.json"
    settings_path.write_text(
        json.dumps(settings, indent=2) + "\n",
        encoding="utf-8",
    )


def write_project_vscode_extensions(target_dir: Path) -> None:
    source_path = package_dir() / ".vscode" / "extensions.json"
    if not source_path.exists():
        return

    vscode_dir = target_dir / ".vscode"
    vscode_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, vscode_dir / "extensions.json")


def write_project_gitignore(target_dir: Path) -> None:
    gitignore_content = """build/
.DS_Store
*.aux
*.acn
*.acr
*.alg
*.bbl
*.bcf
*.blg
*.dvi
*.fdb_latexmk
*.fls
*.glg
*.glo
*.gls
*.idx
*.ilg
*.ind
*.ist
*.lof
*.log
*.lot
*.nav
*.nlo
*.out
*.ps
*.run.xml
*.snm
*.synctex.gz
*.toc
*.vrb
*.xdv
_minted-*/
"""
    (target_dir / ".gitignore").write_text(gitignore_content, encoding="utf-8")


def write_project_setup_scripts(target_dir: Path) -> None:
    scripts_dir = target_dir / "scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)

    setup_py = """#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


BASE_TOOLS = ["latexmk", "lualatex"]
EXTRA_TOOLS = ["bibtex", "biber"]


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def detect_os() -> str:
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    if system == "windows":
        return "windows"
    if system == "linux":
        return "linux"
    return system


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def privilege_prefix() -> list[str]:
    geteuid = getattr(os, "geteuid", None)
    if geteuid is not None and geteuid() == 0:
        return []
    if command_exists("sudo"):
        return ["sudo"]
    return []


def recommended_extensions() -> list[str]:
    extensions_file = project_root() / ".vscode" / "extensions.json"
    if not extensions_file.exists():
        return []

    data = json.loads(extensions_file.read_text(encoding="utf-8"))
    return list(data.get("recommendations", []))


def install_vscode_extensions() -> bool:
    if not command_exists("code"):
        print("VS Code CLI not found: `code` is not in PATH.")
        print("On macOS, open VS Code then run:")
        print("Shell Command: Install 'code' command in PATH")
        return False

    all_ok = True
    for extension in recommended_extensions():
        result = subprocess.run(
            ["code", "--install-extension", extension, "--force"],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"[ok] Extension installed or already present: {extension}")
        else:
            all_ok = False
            stderr = result.stderr.strip() or result.stdout.strip()
            print(f"[warn] Could not install extension {extension}")
            if stderr:
                print(stderr)
    return all_ok


def install_tex_distribution() -> bool:
    current_os = detect_os()

    commands: list[list[str]] = []
    description = ""

    if current_os == "macos":
        if not command_exists("brew"):
            print("Homebrew not found. Cannot install TeX automatically on macOS.")
            print("Install MacTeX manually: https://www.tug.org/mactex/")
            return False
        description = "Installing MacTeX (no GUI apps) via Homebrew"
        commands = [["brew", "install", "--cask", "mactex-no-gui"]]
    elif current_os == "windows":
        if not command_exists("winget"):
            print("winget not found. Cannot install TeX automatically on Windows.")
            print("Install MiKTeX or TeX Live manually.")
            print("MiKTeX: https://miktex.org/howto/install-miktex")
            print("TeX Live: https://www.tug.org/texlive/windows.html")
            return False
        description = "Installing MiKTeX via winget"
        commands = [[
            "winget",
            "install",
            "-e",
            "--id",
            "MiKTeX.MiKTeX",
            "--accept-source-agreements",
            "--accept-package-agreements",
        ]]
    elif current_os == "linux":
        sudo_prefix = privilege_prefix()
        if command_exists("apt-get"):
            description = "Installing full TeX Live via apt"
            commands = [
                [*sudo_prefix, "apt-get", "update"],
                [*sudo_prefix, "apt-get", "install", "-y", "texlive-full", "latexmk", "biber"],
            ]
        elif command_exists("dnf"):
            description = "Installing full TeX Live via dnf"
            commands = [
                [*sudo_prefix, "dnf", "install", "-y", "texlive-scheme-full", "latexmk", "biber"],
            ]
        elif command_exists("pacman"):
            description = "Installing TeX Live via pacman"
            commands = [
                [*sudo_prefix, "pacman", "-S", "--needed", "texlive-meta", "biber"],
            ]
        else:
            print("No supported package manager detected automatically on Linux.")
            print("Install TeX Live manually: https://www.tug.org/texlive/quickinstall.html")
            return False
    else:
        print(f"OS not supported for automatic installation: {current_os}")
        return False

    print(description)
    for command in commands:
        print("")
        print("Running command:")
        print(" ".join(command))
        result = subprocess.run(command, check=False)
        if result.returncode != 0:
            print("")
            print("[warn] Automatic installation failed.")
            return False

    print("")
    print("[ok] Installation commands completed.")
    if current_os == "macos":
        print("On macOS, open a new terminal or run:")
        print('eval "$(/usr/libexec/path_helper)"')
    print("Then restart VS Code before compiling.")
    return True


def print_tool_status() -> tuple[bool, bool]:
    base_ready = True
    extra_ready = True

    print("Checking LaTeX tools:")
    for tool in BASE_TOOLS:
        exists = command_exists(tool)
        print(f"- {tool}: {'ok' if exists else 'missing'}")
        base_ready = base_ready and exists

    print("Tools useful for some templates:")
    for tool in EXTRA_TOOLS:
        exists = command_exists(tool)
        print(f"- {tool}: {'ok' if exists else 'missing'}")
        extra_ready = extra_ready and exists

    return base_ready, extra_ready


def print_os_specific_help() -> None:
    current_os = detect_os()
    print("")
    print("Recommended LaTeX distribution installation:")

    if current_os == "macos":
        print("- OS detected: macOS")
        print("- Recommended: MacTeX")
        print("- Official site: https://www.tug.org/mactex/")
        print("- After installation, restart VS Code then verify:")
        print("  latexmk --version")
        print("  lualatex --version")
    elif current_os == "windows":
        print("- OS detected: Windows")
        print("- Recommended: TeX Live for a stable setup, or MiKTeX for a lighter install.")
        print("- TeX Live: https://www.tug.org/texlive/windows.html")
        print("- MiKTeX: https://miktex.org/howto/install-miktex")
        print("- After installation, restart VS Code then verify:")
        print("  latexmk --version")
        print("  lualatex --version")
    elif current_os == "linux":
        print("- OS detected: Linux")
        print("- Recommended: TeX Live")
        print("- Official guide: https://www.tug.org/texlive/quickinstall.html")
        print("- After installation, restart VS Code then verify:")
        print("  latexmk --version")
        print("  lualatex --version")
    else:
        print(f"- OS detected: {current_os}")
        print("- Install a LaTeX distribution that provides at least `latexmk` and `lualatex`.")


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    check_only = "--check-only" in args
    skip_extensions = "--skip-extensions" in args
    install_tex = "--install-tex" in args

    if check_only and install_tex:
        print("`--check-only` and `--install-tex` cannot be used together.")
        return 2

    print(f"OS detected: {detect_os()}")
    print(f"Python: {sys.executable}")
    print("")

    extensions_ok = True
    if skip_extensions:
        print("VS Code extension installation skipped.")
    elif check_only:
        print("Check-only mode: no VS Code extensions will be installed.")
    else:
        print("Installing recommended VS Code extensions...")
        extensions_ok = install_vscode_extensions()

    print("")
    base_ready, extra_ready = print_tool_status()

    if install_tex and not base_ready:
        print("")
        tex_install_ok = install_tex_distribution()
        print("")
        base_ready, extra_ready = print_tool_status()
        if not tex_install_ok and not base_ready:
            print_os_specific_help()
            print("")
            print("[warn] The LaTeX environment is not yet complete.")
            if not extensions_ok:
                print("[warn] Some VS Code extensions could not be installed automatically.")
            return 1

    print_os_specific_help()

    print("")
    if base_ready:
        print("[ok] The minimal environment for compiling this project is ready.")
        if not extra_ready:
            print("[warn] Some bibliography tools are still missing for certain templates.")
        return 0

    print("[warn] The LaTeX environment is not yet complete.")
    if not extensions_ok:
        print("[warn] Some VS Code extensions could not be installed automatically.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
"""

    setup_sh = """#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if command -v python3 >/dev/null 2>&1; then
  exec python3 "$SCRIPT_DIR/setup.py" "$@"
elif command -v python >/dev/null 2>&1; then
  exec python "$SCRIPT_DIR/setup.py" "$@"
else
  echo "Python 3 is required to run this setup script."
  exit 1
fi
"""

    setup_bat = """@echo off
set SCRIPT_DIR=%~dp0

where py >nul 2>nul
if %ERRORLEVEL%==0 (
  py "%SCRIPT_DIR%setup.py" %*
  exit /b %ERRORLEVEL%
)

where python >nul 2>nul
if %ERRORLEVEL%==0 (
  python "%SCRIPT_DIR%setup.py" %*
  exit /b %ERRORLEVEL%
)

echo Python 3 is required to run this setup script.
exit /b 1
"""

    setup_py_path = scripts_dir / "setup.py"
    setup_sh_path = scripts_dir / "setup.sh"
    setup_bat_path = scripts_dir / "setup.bat"

    setup_py_path.write_text(setup_py, encoding="utf-8")
    setup_sh_path.write_text(setup_sh, encoding="utf-8")
    setup_bat_path.write_text(setup_bat, encoding="utf-8")
    setup_py_path.chmod(0o755)
    setup_sh_path.chmod(0o755)


def create_project(
    name: str,
    template: str,
    output_dir: Path | None = None,
) -> tuple[Path, Path]:
    validate_name(name)

    source_dir = templates_dir() / template
    if not source_dir.is_dir():
        available = ", ".join(available_templates())
        raise ValueError(f"Unknown template: {template}. Available: {available}")

    base_dir = (output_dir or Path.cwd()).resolve()
    target_dir = base_dir / name
    main_tex_file = target_dir / f"{name}.tex"
    local_style_dir = target_dir / "styles" / "packages"

    if target_dir.exists():
        raise FileExistsError(f"Folder already exists: {target_dir}")

    target_dir.mkdir(parents=True, exist_ok=False)
    try:
        copy_tree(source_dir, target_dir)

        copied_main = target_dir / "main.tex"
        if copied_main.exists():
            copied_main.rename(main_tex_file)

        local_style_dir.mkdir(parents=True, exist_ok=True)
        for style_path in required_style_files(source_dir):
            shutil.copy2(style_path, local_style_dir / style_path.name)

        (target_dir / "assets" / "logos").mkdir(parents=True, exist_ok=True)
        for copied_style in local_style_dir.glob("*.sty"):
            patch_local_style(copied_style)

        for logo_path in sorted(logos_dir().iterdir()):
            if should_ignore(logo_path):
                continue
            destination = target_dir / "assets" / "logos" / logo_path.name
            if logo_path.is_dir():
                shutil.copytree(logo_path, destination)
            else:
                shutil.copy2(logo_path, destination)

        (target_dir / "assets" / "logos" / ".gitkeep").touch(exist_ok=True)
        write_project_vscode_settings(target_dir)
        write_project_vscode_extensions(target_dir)
        write_project_gitignore(target_dir)
        write_project_setup_scripts(target_dir)

        from .config import get_profile
        apply_profile_to_metadata(target_dir / "frontmatter" / "metadata.tex", get_profile())
        write_getting_started_guide(target_dir, name, template)
    except Exception:
        shutil.rmtree(target_dir, ignore_errors=True)
        raise

    return target_dir, main_tex_file


def _rename(old_dir: Path, new_name: str) -> tuple[Path, Path]:
    validate_name(new_name)

    new_dir = old_dir.parent / new_name
    old_name = old_dir.name

    if not old_dir.is_dir():
        raise FileNotFoundError(f"Project not found: {old_dir}")
    if new_dir.exists():
        raise FileExistsError(f"Target folder already exists: {new_dir}")

    old_main_tex = old_dir / f"{old_name}.tex"
    new_main_tex = old_dir / f"{new_name}.tex"
    if not old_main_tex.exists():
        raise FileNotFoundError(
            f"Main file not found: {old_main_tex}. "
            "The main file name must match the folder name."
        )

    old_main_tex.rename(new_main_tex)

    build_dir = old_dir / "build"
    if build_dir.is_dir():
        for build_file in build_dir.glob(f"{old_name}.*"):
            build_file.rename(build_dir / f"{new_name}{build_file.suffix}")

    for root_file in old_dir.glob(f"{old_name}.*"):
        if root_file.name == new_main_tex.name:
            continue
        root_file.rename(old_dir / f"{new_name}{root_file.suffix}")

    # Windows: cannot rename a directory that is the current working directory.
    if Path.cwd().resolve() == old_dir.resolve():
        os.chdir(old_dir.parent)
    old_dir.rename(new_dir)
    return new_dir, new_dir / f"{new_name}.tex"


def rename_project(old_name: str, new_name: str) -> tuple[Path, Path]:
    return _rename(Path.cwd().resolve() / old_name, new_name)


def rename_current_project(new_name: str) -> tuple[Path, Path]:
    return _rename(Path.cwd().resolve(), new_name)
