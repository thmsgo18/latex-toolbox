from __future__ import annotations

import json
import os
import re
import shutil
from pathlib import Path


TEMPLATE_DESCRIPTIONS: dict[str, str] = {
    "cv-en": "CV / résumé — education, experience, projects, involvement, skills",
    "cv-fr": "CV — formation, expérience, projets, engagement, compétences",
    "project-report-en": "Project report — ISO/IEEE (requirements, architecture, testing, bibliography, appendices)",
    "project-report-fr": "Rapport de projet — AFNOR/ISO (cahier des charges, architecture, tests, bibliographie, annexes)",
    "research": "Research article — two-column (related work, methodology, experiments, bibliography)",
}

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


def _write_cv_getting_started(target_dir: Path, name: str, template: str) -> None:
    is_fr = template == "cv-fr"

    if is_fr:
        heading_file = "sections/en-tete.tex"
        section_table = """\
| `sections/en-tete.tex` | Nom, contacts, résumé |
| `sections/formation.tex` | Diplômes et formations |
| `sections/experience.tex` | Expériences professionnelles |
| `sections/projets.tex` | Projets personnels et académiques |
| `sections/engagement.tex` | Engagements et associations |
| `sections/competences.tex` | Compétences techniques et langues |"""
        add_exp_title = "### Ajouter une expérience"
        add_exp_body = f"""\
Dans `sections/experience.tex`, ajoutez un bloc `\\resumeSubheading` :

```latex
\\resumeSubheading
  {{Intitulé du poste}}{{mois 20XX -- mois 20XX}}
  {{Nom de l'entreprise}}{{Ville, France}}
  \\begin{{itemize}}[leftmargin=0.12in, label={{}}, itemsep=0pt]
    \\item \\small Description de vos missions.
  \\end{{itemize}}
```"""
        add_proj_title = "### Ajouter un projet"
        add_proj_body = f"""\
Dans `sections/projets.tex`, ajoutez un bloc `\\resumeProjectHeading` :

```latex
\\resumeProjectHeading
  {{\\textbf{{\\href{{https://github.com/username/projet}}{{Nom -- Technologies}}}}}}{{Contexte}}
  \\begin{{itemize}}[leftmargin=0.12in, label={{}}, itemsep=0pt]
    \\item \\small Description du projet.
  \\end{{itemize}}
```"""
        workflow_step1 = f"Ouvrez `{heading_file}` et renseignez votre nom, téléphone, email et liens GitHub/LinkedIn."
        workflow_step2 = "Éditez les fichiers dans `sections/` — un fichier par rubrique."
        workflow_step3 = f"Sauvegardez `{name}.tex` dans VS Code → LaTeX Workshop compile automatiquement → PDF dans `build/{name}.pdf`."
        fail_font = "**Police introuvable** → vérifiez que TeX Live est à jour : `tlmgr update --all`"
        resources_title = "## Ressources"
    else:
        heading_file = "sections/heading.tex"
        section_table = """\
| `sections/heading.tex` | Name, contacts, summary |
| `sections/education.tex` | Degrees and education |
| `sections/experience.tex` | Work experience |
| `sections/projects.tex` | Personal and academic projects |
| `sections/involvement.tex` | Volunteering and associations |
| `sections/skills.tex` | Technical skills and languages |"""
        add_exp_title = "### Add a work experience"
        add_exp_body = f"""\
In `sections/experience.tex`, add a `\\resumeSubheading` block:

```latex
\\resumeSubheading
  {{Job Title}}{{Month 20XX -- Month 20XX}}
  {{Company Name}}{{City, Country}}
  \\begin{{itemize}}[leftmargin=0.12in, label={{}}, itemsep=0pt]
    \\item \\small Description of your responsibilities.
  \\end{{itemize}}
```"""
        add_proj_title = "### Add a project"
        add_proj_body = f"""\
In `sections/projects.tex`, add a `\\resumeProjectHeading` block:

```latex
\\resumeProjectHeading
  {{\\textbf{{\\href{{https://github.com/username/project}}{{Name -- Technologies}}}}}}{{Context}}
  \\begin{{itemize}}[leftmargin=0.12in, label={{}}, itemsep=0pt]
    \\item \\small Project description.
  \\end{{itemize}}
```"""
        workflow_step1 = f"Open `{heading_file}` and fill in your name, phone, email and GitHub/LinkedIn links."
        workflow_step2 = "Edit the files in `sections/` — one file per section."
        workflow_step3 = f"Save `{name}.tex` in VS Code → LaTeX Workshop compiles automatically → PDF in `build/{name}.pdf`."
        fail_font = "**Font not found** → make sure TeX Live is up to date: `tlmgr update --all`"
        resources_title = "## Resources"

    content = f"""\
# Getting Started — {name}

## Workflow

**1. {'Modifier vos informations' if is_fr else 'Edit your personal information'}**

{workflow_step1}

**2. {'Remplir chaque section' if is_fr else 'Fill in each section'}**

{workflow_step2}

**3. {'Sauvegarder pour compiler' if is_fr else 'Save to compile'}**

{workflow_step3}

---

## {'Structure des sections' if is_fr else 'Section structure'}

| {'Fichier' if is_fr else 'File'} | {'Contenu' if is_fr else 'Content'} |
|---|---|
{section_table}

---

## {'Opérations courantes' if is_fr else 'Common operations'}

{add_exp_title}

{add_exp_body}

{add_proj_title}

{add_proj_body}

---

## {'Si la compilation échoue' if is_fr else 'If compilation fails'}

1. **{'LaTeX non installé' if is_fr else 'LaTeX not installed'}** → `latex-forge setup --install-tex`
2. **{'LaTeX Workshop non installé' if is_fr else 'LaTeX Workshop not installed'}** → {'installer depuis le panneau Extensions de VS Code' if is_fr else 'install from the VS Code Extensions panel'}
3. {fail_font}
4. **{'Compilation bloquée' if is_fr else 'Compilation stuck'}** → {'supprimer le dossier' if is_fr else 'delete the'} `build/` {'et réessayer' if is_fr else 'folder and try again'}

{'Ce CV' if is_fr else 'This CV'} {'utilise' if is_fr else 'uses'} **LuaLaTeX** ({'pour fontspec' if is_fr else 'for fontspec'}). {'Vérifiez' if is_fr else 'Verify'}:

```bash
lualatex --version
```

---

{resources_title}

| {'Ressource' if is_fr else 'Resource'} | Lien |
|---|---|
| Overleaf — {'Modèles de CV' if is_fr else 'CV templates'} | <https://www.overleaf.com/gallery/tagged/cv> |
| LaTeX Wikibook | <https://en.wikibooks.org/wiki/LaTeX> |
| fontawesome5 {'icônes' if is_fr else 'icons'} | <https://mirrors.ctan.org/fonts/fontawesome5/doc/fontawesome5.pdf> |
"""
    (target_dir / "GETTING_STARTED.md").write_text(content, encoding="utf-8")


def write_agents_md(target_dir: Path, name: str, template: str) -> None:
    """Generate AGENTS.md — a self-contained briefing for any AI working on the project."""

    is_cv = template in ("cv-fr", "cv-en")
    is_fr_cv = template == "cv-fr"
    has_bibliography = template in ("project-report-fr", "project-report-en", "research")
    description = TEMPLATE_DESCRIPTIONS.get(template, template)

    # ── Compilation section ────────────────────────────────────────────────
    if has_bibliography:
        compile_manual = f"""\
```bash
lualatex -interaction=nonstopmode -output-directory=build {name}.tex
biber build/{name}
lualatex -interaction=nonstopmode -output-directory=build {name}.tex
lualatex -interaction=nonstopmode -output-directory=build {name}.tex
```"""
    else:
        compile_manual = f"""\
```bash
lualatex -interaction=nonstopmode -output-directory=build {name}.tex
lualatex -interaction=nonstopmode -output-directory=build {name}.tex
```"""

    # ── File structure table ───────────────────────────────────────────────
    if is_cv:
        if is_fr_cv:
            structure_rows = """\
| `{name}.tex` | Point d'entrée — ne pas modifier la structure |
| `sections/en-tete.tex` | **Commencer ici** — nom, contacts, résumé |
| `sections/formation.tex` | Diplômes et formations |
| `sections/experience.tex` | Expériences professionnelles |
| `sections/projets.tex` | Projets personnels et académiques |
| `sections/engagement.tex` | Engagements et associations |
| `sections/competences.tex` | Compétences techniques et langues |
| `styles/packages/cv.sty` | Style LuaLaTeX/fontspec — **NE PAS MODIFIER** |
| `build/` | PDF compilé — généré automatiquement |"""
        else:
            structure_rows = """\
| `{name}.tex` | Entry point — do not change the structure |
| `sections/heading.tex` | **Start here** — name, contacts, summary |
| `sections/education.tex` | Degrees and education |
| `sections/experience.tex` | Work experience |
| `sections/projects.tex` | Personal and academic projects |
| `sections/involvement.tex` | Volunteering and associations |
| `sections/skills.tex` | Technical skills and languages |
| `styles/packages/cv.sty` | LuaLaTeX/fontspec style — **DO NOT EDIT** |
| `build/` | Compiled PDF — auto-generated |"""
    elif template == "research":
        structure_rows = """\
| `{name}.tex` | Entry point — do not change the structure |
| `frontmatter/metadata.tex` | Title, authors, abstract, keywords |
| `sections/` | Content — one .tex file per section |
| `references/references.bib` | BibTeX bibliography file |
| `appendix/` | Appendices and supplementary material |
| `styles/packages/` | Style files — **DO NOT EDIT** |
| `build/` | Compiled PDF — auto-generated |"""
    else:
        bib_folder = "bibliography/"
        structure_rows = """\
| `{name}.tex` | Point d'entrée / Entry point — do not change the structure |
| `frontmatter/metadata.tex` | Titre, auteurs, résumé, mots-clés |
| `sections/` | Contenu — un fichier .tex par section |
| `backmatter/` | Déclaration IA, remerciements, fin de document |
| `images/` | Fichiers images (PNG, JPG, PDF) |
| `figures/` | Figures TikZ/pgfplots (sources LaTeX) |
| `assets/logos/` | Logos université et projet |
| `{bib_folder}references.bib` | Fichier de références BibTeX |
| `styles/packages/` | Fichiers de style — **NE PAS MODIFIER** |
| `build/` | PDF compilé — généré automatiquement |"""

    structure_rows = structure_rows.replace("{name}", name).replace("{bib_folder}", "bibliography/")

    # ── Custom commands ────────────────────────────────────────────────────
    if is_cv:
        custom_commands = """\
| Command | Description |
|---|---|
| `\\resumeSubheading{title}{date}{subtitle}{location}` | Standard CV entry (job, degree…) |
| `\\resumeProjectHeading{\\textbf{\\href{url}{Name -- Tech}}}{Context}` | Project entry with link |
| `\\resumeSubHeadingListStart` / `\\resumeSubHeadingListEnd` | Wrap a group of entries |
| `\\myuline{text}` | Custom underline (used in heading links) |"""
    elif template == "research":
        custom_commands = """\
| Command | Description |
|---|---|
| `\\startannexes` | Opens the Appendices section with lettered subsections (A, B, C…) |"""
    else:
        custom_commands = """\
| Command | Description |
|---|---|
| `\\startannexes` | Opens the Annexes/Appendices section with lettered subsections (A, B, C…) |
| `\\addauthor{Name}{}[github]` | Adds an author to the cover page (in `frontmatter/metadata.tex`) |"""

    # ── How to add content ─────────────────────────────────────────────────
    if is_cv:
        if is_fr_cv:
            add_content = """\
### Ajouter une expérience

Dans `sections/experience.tex` :
```latex
\\resumeSubheading
  {Intitulé du poste}{mois 20XX -- mois 20XX}
  {Entreprise}{Ville, France}
  \\begin{itemize}[leftmargin=0.12in, label={}, itemsep=0pt]
    \\item \\small Description des missions.
  \\end{itemize}
```

### Ajouter un projet

Dans `sections/projets.tex` :
```latex
\\resumeProjectHeading
  {\\textbf{\\href{https://github.com/user/repo}{Nom -- Technologies}}}{Contexte}
  \\begin{itemize}[leftmargin=0.12in, label={}, itemsep=0pt]
    \\item \\small Description.
  \\end{itemize}
```"""
        else:
            add_content = """\
### Add a work experience

In `sections/experience.tex`:
```latex
\\resumeSubheading
  {Job Title}{Month 20XX -- Month 20XX}
  {Company}{City, Country}
  \\begin{itemize}[leftmargin=0.12in, label={}, itemsep=0pt]
    \\item \\small Description of responsibilities.
  \\end{itemize}
```

### Add a project

In `sections/projects.tex`:
```latex
\\resumeProjectHeading
  {\\textbf{\\href{https://github.com/user/repo}{Name -- Technologies}}}{Context}
  \\begin{itemize}[leftmargin=0.12in, label={}, itemsep=0pt]
    \\item \\small Description.
  \\end{itemize}
```"""
    else:
        if template == "research":
            bib_file = "references/references.bib"
        else:
            bib_file = "bibliography/references.bib"

        add_content = f"""\
### Add a new section

1. Create `sections/my-section.tex`
2. Add `\\input{{sections/my-section.tex}}` at the right place in `{name}.tex`

### Add a bibliography reference

Add an entry to `{bib_file}`, then cite inline:
```latex
As shown in previous work~\\cite{{author2024}}.
```

### Add appendices

Place `\\startannexes` in `{name}.tex` where the appendices begin, then use `\\subsection{{...}}` for each appendix (A, B, C…).

### Add an image

Place the file in `images/`, then:
```latex
\\begin{{figure}}[h]
  \\centering
  \\includegraphics[width=0.8\\linewidth]{{my-image.png}}
  \\caption{{Caption here.}}
  \\label{{fig:my-label}}
\\end{{figure}}
```"""

    # ── Common errors ──────────────────────────────────────────────────────
    bib_errors = ""
    if has_bibliography:
        bib_errors = """\
| `biber` not found | `tlmgr install biber` |
| Bibliography not showing | Run `biber build/{name}` after the first lualatex pass |
| `I found no \\bibdata command` | You ran `bibtex` instead of `biber` — use `biber` |
""".replace("{name}", name)

    common_errors = f"""\
| Error | Fix |
|---|---|
| LaTeX not installed | `latex-forge setup --install-tex` |
| `Package X not found` | `tlmgr install X` |
| Font not found | `tlmgr update --all` or install the missing font package |
{bib_errors}| Compilation stuck / blank pages | Delete `build/` then recompile |
| `Undefined control sequence \\X` | Check `styles/packages/` files are present |
| PDF viewer shows duplicate page | VS Code PDF viewer in "Two Page" mode — switch to "Single Page" |"""

    # ── Assemble ───────────────────────────────────────────────────────────
    lang_note = "French" if template in ("cv-fr", "project-report-fr") else "English"

    content = f"""\
# AGENTS.md — {name}

> Briefing for any AI assistant working on this project.
> Read this file before making any changes.

## Project overview

| Field | Value |
|---|---|
| Template | `{template}` — {description} |
| Language | {lang_note} |
| LaTeX engine | LuaLaTeX |
| Bibliography | {"biblatex + biber" if has_bibliography else "none"} |
| Output | `build/{name}.pdf` |

---

## Compilation

### Automatic (VS Code saves trigger this)

LaTeX Workshop is configured to run on save via `.vscode/settings.json`.
Recipe: `lualatexmk` → output in `build/`.

### Manual

```bash
# Recommended — handles bibliography passes automatically
latexmk -lualatex -interaction=nonstopmode -outdir=build {name}.tex
```

If `latexmk` is unavailable, run the full sequence manually:

{compile_manual}

---

## File structure

| Path | Purpose |
|---|---|
{structure_rows}

---

## Custom LaTeX commands

{custom_commands}

---

## How to add content

{add_content}

---

## Common errors and fixes

{common_errors}

---

## Do not modify

- `styles/packages/*.sty` — managed by latex-forge; edits will be overwritten on reinstall
- `assets/logos/` — logo assets
- The `\\input` / `\\include` order in `{name}.tex` (section order matters for cross-references)

---

## Rename this project

```bash
latex-forge rename new-name
```

Renames the folder, the main `.tex` file, and build artifacts consistently.
"""
    (target_dir / "AGENTS.md").write_text(content, encoding="utf-8")


def write_getting_started_guide(target_dir: Path, name: str, template: str) -> None:
    if template in ("cv-fr", "cv-en"):
        _write_cv_getting_started(target_dir, name, template)
        return

    # Template-specific sections
    _BIBLIOGRAPHY = {
        "research": """\

### Add a bibliography reference

Add your reference to `references/references.bib`, then cite it in your text:

```latex
This result has been demonstrated in prior work~\\cite{author2024}.
```

The bibliography is printed automatically at the end of the document.
""",
        "project-report-fr": """\

### Ajouter une référence bibliographique

Ajoutez votre référence dans `bibliography/references.bib`, puis citez-la dans le texte :

```latex
Ce résultat a été démontré dans des travaux antérieurs~\\cite{auteur2024}.
```

La bibliographie apparaît automatiquement avant les annexes.
""",
        "project-report-en": """\

### Add a bibliography reference

Add your reference to `bibliography/references.bib`, then cite it in your text:

```latex
This result has been demonstrated in prior work~\\cite{author2024}.
```

The bibliography appears automatically before the appendices.
""",
    }

    _EXTRA_FOLDERS = {
        "research": "| `references/` | BibTeX reference file |\n"
                    "| `appendix/` | Appendices and supplementary material |\n",
        "project-report-fr": "| `bibliography/` | Fichier de références BibTeX |\n",
        "project-report-en": "| `bibliography/` | BibTeX reference file |\n",
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
latex-forge rename new-name
```

This renames the folder, the main `.tex` file, and any build artifacts.

---

## If compilation fails

1. **LaTeX not installed** → run `latex-forge setup --install-tex`
2. **LaTeX Workshop not installed** → install it from the VS Code extensions panel
3. **Missing package** → `tlmgr install package-name` (TeX Live) or let MiKTeX auto-install
4. **Compilation stuck** → delete the `build/` folder and try again

This project uses **LuaLaTeX**. Verify it is available:

```bash
lualatex --version
```

---

## Resources

### Official documentation

| Resource | Link |
|---|---|
| LaTeX Project | <https://www.latex-project.org/help/documentation/> |
| CTAN — package index | <https://www.ctan.org> |
| TeXdoc — search package docs | <https://texdoc.org> |
| TikZ & PGF manual | <https://tikz.dev> |

### Learn LaTeX

| Resource | Link |
|---|---|
| Overleaf — Learn LaTeX in 30 minutes | <https://www.overleaf.com/learn/latex/Learn_LaTeX_in_30_minutes> |
| Overleaf knowledge base | <https://www.overleaf.com/learn> |
| LaTeX Wikibook | <https://en.wikibooks.org/wiki/LaTeX> |
| LaTeX FAQ | <https://texfaq.org> |

### LuaLaTeX specific

| Resource | Link |
|---|---|
| LuaLaTeX wiki | <https://www.luatex.org/documentation.html> |
| fontspec (font loading) | <https://texdoc.org/serve/fontspec/0> |
"""
    (target_dir / "GETTING_STARTED.md").write_text(content, encoding="utf-8")


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


def user_templates_dir() -> Path:
    """Directory where user-installed templates are stored."""
    return Path.home() / ".latex-forge" / "templates"


def styles_dir() -> Path:
    return package_dir() / "styles" / "packages"


def logos_dir() -> Path:
    return package_dir() / "assets" / "logos"


def available_templates() -> list[str]:
    built_in = {p.name for p in templates_dir().iterdir() if p.is_dir()}
    user_dir = user_templates_dir()
    user = {p.name for p in user_dir.iterdir() if p.is_dir()} if user_dir.exists() else set()
    return sorted(built_in | user)


def _find_template_source(template: str) -> Path:
    """Resolve a template name to its source directory (built-in or user-installed)."""
    built_in = templates_dir() / template
    if built_in.is_dir():
        return built_in
    user = user_templates_dir() / template
    if user.is_dir():
        return user
    available = ", ".join(available_templates())
    raise ValueError(f"Unknown template: {template}. Available: {available}")


def _read_template_engine(source_dir: Path) -> str:
    """Read the LaTeX engine from latexforge.toml in the template directory.

    Returns one of 'lualatex', 'xelatex', 'pdflatex'. Defaults to 'lualatex'.
    """
    toml_path = source_dir / "latexforge.toml"
    if not toml_path.exists():
        return "lualatex"
    for line in toml_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("engine"):
            parts = line.split("=", 1)
            if len(parts) == 2:
                value = parts[1].strip().strip('"').strip("'")
                if value in ("lualatex", "xelatex", "pdflatex"):
                    return value
    return "lualatex"


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


_ENGINE_LATEXMK_FLAG = {
    "lualatex": "-lualatex",
    "xelatex": "-xelatex",
    "pdflatex": "-pdf",
}


def write_project_vscode_settings(target_dir: Path, engine: str = "lualatex") -> None:
    vscode_dir = target_dir / ".vscode"
    vscode_dir.mkdir(parents=True, exist_ok=True)

    latexmk_flag = _ENGINE_LATEXMK_FLAG.get(engine, "-lualatex")
    tool_name = f"{engine}mk"

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
                "name": tool_name,
                "command": "latexmk",
                "args": [
                    "-synctex=1",
                    "-interaction=nonstopmode",
                    "-file-line-error",
                    latexmk_flag,
                    "-outdir=%OUTDIR%",
                    "%DOC%",
                ],
            }
        ],
        "latex-workshop.latex.recipes": [
            {"name": tool_name, "tools": [tool_name]}
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

    source_dir = _find_template_source(template)

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
        engine = _read_template_engine(source_dir)
        write_project_vscode_settings(target_dir, engine)
        write_project_vscode_extensions(target_dir)
        write_project_gitignore(target_dir)
        write_project_setup_scripts(target_dir)

        write_getting_started_guide(target_dir, name, template)
        write_agents_md(target_dir, name, template)
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
