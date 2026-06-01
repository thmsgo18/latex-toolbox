<div align="center">

# LaTeX Toolbox

Skip the setup. Start writing. Everything you need, nothing more.

[![PyPI version](https://img.shields.io/pypi/v/latex-toolbox?color=blue)](https://pypi.org/project/latex-toolbox/)
[![CI](https://github.com/thmsgo18/latex-toolbox/actions/workflows/ci.yml/badge.svg)](https://github.com/thmsgo18/latex-toolbox/actions/workflows/ci.yml)
[![Python](https://img.shields.io/pypi/pyversions/latex-toolbox)](https://pypi.org/project/latex-toolbox/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

[Lire en français](./README.fr.md)

</div>

---

LaTeX Toolbox is a command-line tool that generates ready-to-compile, standalone LaTeX projects from templates. Each generated project embeds its own styles and assets — it can be compiled, shared, and versioned independently, with no dependency on this repository.

## Installation

```bash
pipx install latex-toolbox
```

Requires Python 3.10+. If `pipx` is not installed: `brew install pipx` on macOS, or see [pipx.pypa.io](https://pipx.pypa.io).

## First setup

On a fresh machine, run the setup command to check your environment and install LaTeX automatically:

```bash
latex-toolbox setup
```

This verifies that `latexmk` and `lualatex` are available, and offers to install them via your system package manager (`brew` on macOS, `apt` on Debian/Ubuntu, `winget` on Windows). VS Code extensions are also installed if the `code` CLI is available.

## Usage

### Interactive mode

Run `create` with no arguments to be guided step by step:

```
$ latex-toolbox create

Project name: my-report
Available templates:
  1. rapport-projet-en
  2. rapport-projet-fr
  3. rapport-ter
  4. research
Choose a template [1-4]: 1
Create project in [/Users/thomas/Desktop]:

Project created: /Users/thomas/Desktop/my-report
Edit: my-report/my-report.tex
Next: fill in frontmatter/metadata.tex then save to compile.
Open project in VS Code? [y/N]
```

### With flags

All arguments are optional — omitted ones are prompted interactively.

```bash
# specify everything upfront
latex-toolbox create --name my-report --template rapport-projet-en

# create in a specific directory
latex-toolbox create --name my-paper --template research --output ~/Desktop
```

### Rename a project

```bash
# from the parent directory
latex-toolbox rename old-name new-name

# from inside the project directory
latex-toolbox rename new-name
```

This renames the folder, the main `.tex` file, and any existing build artifacts.

## Available templates

| Template | Language | Description |
|---|---|---|
| `rapport-projet-en` | English | Project report with cover page, TOC, introduction, conclusion, AI statement |
| `rapport-projet-fr` | French | Same structure as above, in French |
| `rapport-ter` | English | Academic TER report with detailed structure, bibliography, and appendices |
| `research` | English | Research article with two-column layout, abstract, and BibTeX bibliography |

```bash
latex-toolbox list-templates
```

## After creating a project

1. Open the generated folder in VS Code.
2. Fill in `frontmatter/metadata.tex` — title, authors, course name, university logo.
3. Save the main `.tex` file to trigger compilation (requires [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop)).
4. The PDF is built into `build/`.

Example `metadata.tex`:

```tex
\newcommand{\reporttitle}{Audio Fingerprinting Study}
\newcommand{\coursename}{Machine Learning}

\resetauthors
\addauthor{Alice Martin}{}
\addauthor{Bob Durand}{}

\resetteachers
\addteacher{Dr Example}{}

\resetprojectlinks
\addprojectlink{Repository}{https://github.com/example/project}
```

Leaving the second argument empty in `\addauthor{...}{}` or `\addteacher{...}{}` hides the role label.

## Generated project structure

```
my-project/
├── my-project.tex            ← main file (named after the project)
├── frontmatter/
│   ├── metadata.tex          ← title, authors, course
│   └── toc.tex
├── sections/
├── backmatter/
├── figures/
├── images/
├── screens/
├── assets/
│   ├── images/common/
│   └── logos/
├── styles/packages/          ← embedded styles, no external dependency
├── scripts/                  ← standalone setup scripts
├── .vscode/                  ← LaTeX Workshop settings
└── .gitignore
```

Styles and logos are copied into the project at creation time. The generated project has no runtime dependency on this repository.

## Command reference

| Command | Description |
|---|---|
| `latex-toolbox create` | Create a project (interactive) |
| `latex-toolbox create --name NAME --template TEMPLATE` | Create with explicit arguments |
| `latex-toolbox create --output DIR` | Set output directory |
| `latex-toolbox rename OLD NEW` | Rename from parent directory |
| `latex-toolbox rename NEW` | Rename from inside project directory |
| `latex-toolbox list-templates` | List available templates |
| `latex-toolbox setup` | Check and set up the LaTeX environment |
| `latex-toolbox setup --check-only` | Check without installing anything |
| `latex-toolbox setup --install-tex` | Install LaTeX directly |
| `latex-toolbox --version` | Show installed version |

## Versioning generated projects

Each generated project is self-contained, making it straightforward to version independently:

```bash
cd my-project
git init
git add .
git commit -m "Initial report"
```

Create a dedicated private repository and invite only the collaborators relevant to that document.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
