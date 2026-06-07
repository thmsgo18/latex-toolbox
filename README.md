# LaTeX Forge

<p align="center">
  <img src="docs/assets/latex-forge-logo.png" alt="LaTeX Forge" width="480">
</p>

<p align="center">
  Create professional documents. Save. Your PDF appears instantly.
</p>

<p align="center">
  <a href="https://pypi.org/project/latex-forge/"><img src="https://img.shields.io/pypi/v/latex-forge?style=for-the-badge&color=blue" alt="PyPI version"></a>
  <a href="https://github.com/thmsgo18/latex-forge/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/thmsgo18/latex-forge/ci.yml?branch=main&style=for-the-badge" alt="CI"></a>
  <a href="https://pypi.org/project/latex-forge/"><img src="https://img.shields.io/pypi/pyversions/latex-forge?style=for-the-badge" alt="Python versions"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="License MIT"></a>
</p>

<p align="center">
  <a href="./README.fr.md">Lire en français</a>
</p>

---

One command creates a ready-to-write document project. Open it in VS Code, start writing, save — your PDF rebuilds and appears in a side panel automatically. No manual compilation, no window switching.

Works for humans and AI agents alike. Every generated project includes an `AGENTS.md` that briefs any AI assistant on the document structure, so it can contribute immediately.

## How it feels

<p align="center">
  <img src="docs/assets/live-preview.png" alt="LaTeX Forge live preview in VS Code" width="800">
</p>

Write on one side. See your document on the other. Every save refreshes the result.

## Quick start

```bash
# 1 — install
pipx install latex-forge

# 2 — set up your environment (LaTeX + VS Code extensions)
latex-forge setup

# 3 — create a project
latex-forge create --name my-report --template rapport-projet-en

# 4 — open and start writing
code my-report
```

Requires Python 3.10+. If `pipx` is not installed: `brew install pipx` on macOS, or see [pipx.pypa.io](https://pipx.pypa.io).

## Installation

```bash
pipx install latex-forge
```

## First setup

On a fresh machine, run the setup command to verify your environment and install what's missing:

```bash
latex-forge setup
```

This checks for `latexmk` and `lualatex`, and offers to install them automatically (`brew` on macOS, `apt` on Debian/Ubuntu, `winget` on Windows). VS Code extensions are installed too if the `code` CLI is available.

## Profile

Set up your profile once. Every project you create after that will have your name, university, and program pre-filled:

```bash
latex-forge profile --set
```

```
Full name: Dupont Alice
University / school: Université de Bordeaux
Program / formation: Master Informatique
GitHub username (optional): dupont-alice
```

```bash
latex-forge profile        # view current profile
latex-forge profile --set  # update
```

Profile values are stored in `~/.latex-forge.toml` and injected into each new project's `frontmatter/metadata.tex`.

## Shell completion

Tab completion for commands, flags, and template names:

**bash** (`~/.bashrc`) or **zsh** (`~/.zshrc`):

```bash
eval "$(latex-forge completion)"
```

## Configuration

```toml
# ~/.latex-forge.toml
default_template = "rapport-projet-en"
default_output_dir = "~/Documents/projects"
```

| Key | Description |
|---|---|
| `default_template` | Template used when `--template` is omitted |
| `default_output_dir` | Output directory used when `--output` is omitted |

## Usage

### Interactive mode

```
$ latex-forge create

Project name: my-report
Available templates:
  1. cv-en
  2. cv-fr
  3. rapport-projet-en
  4. rapport-projet-fr
  5. research
Choose a template [1-5]: 3
Create project in [/Users/alice/Desktop]:

Project created: /Users/alice/Desktop/my-report
Open project in VS Code? [y/N]
```

### With flags

```bash
latex-forge create --name my-report --template rapport-projet-en
latex-forge create --name my-paper --template research --output ~/Desktop
```

### Rename a project

```bash
latex-forge rename old-name new-name   # from parent directory
latex-forge rename new-name            # from inside the project
```

## Built-in templates

| Template | Language | Description |
|---|---|---|
| `rapport-projet-en` | English | ISO/IEEE project report — requirements, architecture, testing, bibliography |
| `rapport-projet-fr` | French | AFNOR/ISO project report — cahier des charges, architecture, tests, bibliographie |
| `research` | English | Two-column research article — related work, methodology, experiments, bibliography |
| `cv-en` | English | CV / résumé — education, experience, projects, skills |
| `cv-fr` | French | CV — formation, expérience, projets, compétences |

```bash
latex-forge list-templates
```

## Template gallery

More document types are available in the [latex-forge-gallery](https://github.com/thmsgo18/latex-forge-gallery): CVs, theses, articles, presentations, posters, and more.

```bash
# install any template directly by URL
latex-forge template install https://github.com/thmsgo18/latex-forge-gallery/tree/main/templates/thesis/clean-thesis

# create a project from it
latex-forge create --template clean-thesis --name my-thesis

# manage installed templates
latex-forge template list
latex-forge template remove clean-thesis
```

## Filling in your project

Open `frontmatter/metadata.tex` to set the title, authors, and course:

```tex
\newcommand{\reporttitle}{Audio Fingerprinting Study}
\newcommand{\coursename}{Machine Learning}

\resetauthors
\addauthor{Alice Martin}{}
\addauthor{Bob Durand}{}

\resetteachers
\addteacher{Dr Example}{}
```

Save the main `.tex` file — the PDF rebuilds instantly in VS Code.

## Generated project structure

```
my-project/
├── my-project.tex            ← main file (renamed from the project name)
├── frontmatter/
│   ├── metadata.tex          ← title, authors, course — start here
│   └── toc.tex
├── sections/                 ← one .tex file per section
├── backmatter/               ← acknowledgements, appendices
├── bibliography/
│   └── references.bib
├── figures/
├── images/
├── assets/logos/
├── styles/packages/          ← embedded styles, no external dependency
├── .vscode/                  ← pre-configured for live PDF preview
├── AGENTS.md                 ← AI briefing for this document
└── .gitignore
```

The project is fully self-contained: styles and assets are copied in at creation time. It compiles, shares, and versions independently — no dependency on this repository.

## AI-friendly by design

Every generated project includes `AGENTS.md` — a self-contained briefing that tells any AI assistant exactly what the project contains, how to compile it, how to add content, and what not to touch. An AI can open a project cold and contribute correctly without any extra context.

## Command reference

| Command | Description |
|---|---|
| `latex-forge create` | Create a project (interactive) |
| `latex-forge create --name NAME --template TEMPLATE` | Create with explicit arguments |
| `latex-forge create --output DIR` | Set output directory |
| `latex-forge rename OLD NEW` | Rename from parent directory |
| `latex-forge rename NEW` | Rename from inside project |
| `latex-forge list-templates` | List available templates |
| `latex-forge setup` | Check and set up the environment |
| `latex-forge setup --check-only` | Check without installing |
| `latex-forge setup --install-tex` | Install LaTeX |
| `latex-forge profile` | View saved profile |
| `latex-forge profile --set` | Set up profile |
| `latex-forge template install URL` | Install a template |
| `latex-forge template list` | List all templates |
| `latex-forge template remove NAME` | Remove an installed template |
| `latex-forge completion` | Print shell completion code |
| `latex-forge --version` | Show version |

## Versioning

Each project is self-contained — version it independently:

```bash
cd my-project
git init
git add .
git commit -m "Initial report"
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

Made by [thmsgo18](https://github.com/thmsgo18)
