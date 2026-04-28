# LaTeX Toolbox

[Read this in French](./README.fr.md)

LaTeX Toolbox is a local toolkit for creating polished, reusable, standalone LaTeX projects from ready-made templates.

It is built for a simple workflow:
- keep your templates, styles, and shared assets in this repository;
- generate a new project with the `latex-toolbox` command;
- work on the generated project in VS Code;
- version each generated project in its own Git repository if needed.

If you regularly write course reports, research papers, TER reports, or collaborative LaTeX documents, this repository gives you a clean starting point every time without rebuilding your structure from scratch.

## What the toolbox does

When you create a project, the toolbox:
- copies the selected template;
- renames the main `.tex` file to match the project name;
- copies the required LaTeX styles into the project;
- copies the logos from `assets/logos/`;
- creates a project that can compile on its own.

Generated projects do not depend on this repository at compile time.

## Requirements

Recommended setup:
- Python 3
- a LaTeX distribution such as `MacTeX`
- VS Code
- the `LaTeX Workshop` extension

Useful VS Code extensions:
- `LaTeX Workshop`
- `LTeX+`
- `Code Spell Checker`

Important:
- if you use `LaTeX Workshop`, disable `vscode-pdf` to avoid PDF viewer conflicts.

## Install the command

The easiest installation method is `pipx`.

From this repository root:

```bash
cd /path/to/latex-toolbox
brew install pipx
pipx install --editable .
```

After that, the command is available as:

```bash
latex-toolbox
```

If the command is not found after installation:

```bash
pipx ensurepath
```

Then open a new terminal window.

## Quick start

Create a project report in the current directory:

```bash
latex-toolbox create --name signal-processing-report --template rapport-projet-en
```

Create a research-style paper:

```bash
latex-toolbox create --name audio-search-paper --template research
```

Then open the generated folder in VS Code and start editing the main file:

```text
./signal-processing-report/signal-processing-report.tex
```

## Available commands

List templates:

```bash
latex-toolbox list-templates
```

Create a project:

```bash
latex-toolbox create --name my-project --template rapport-projet-en
```

Rules:
- `--name` is required
- `--template` is required
- the project is created in the current directory
- the created folder uses the project name

Example:

```bash
cd ~/Desktop
latex-toolbox create --name shazam-report --template research
```

This creates:

```text
~/Desktop/shazam-report/
```

## Recommended workflow

### 1. Create a project

```bash
latex-toolbox create --name my-project --template rapport-projet-en
```

Real examples:

```bash
latex-toolbox create --name deep-learning-lab --template rapport-projet-en
latex-toolbox create --name rapport-analyse-signaux --template rapport-projet-fr
latex-toolbox create --name keyword-spotting-paper --template research
```

### 2. Open the project in VS Code

Open the main file, for example:

```text
./my-project/my-project.tex
```

### 3. Fill in the metadata

Cover-page information is centralized in:

```text
frontmatter/metadata.tex
```

Typical values include:
- report title
- course name
- authors
- supervisors
- project links
- university logo

Example:

```tex
\newcommand{\reporttitle}{Audio Fingerprinting Study}
\newcommand{\coursename}{Machine Learning}

\resetauthors
\addauthor{Alice Martin}{}
\addauthor{Bob Durand}{}

\resetteachers
\addteacher{Dr Example}{}

\resetprojectlinks
\addprojectlink{Repository}{https://github.com/example/audio-fingerprinting}
```

If you leave the second argument empty in `\addauthor{...}{}` or `\addteacher{...}{}`, no role is displayed.

### 4. Compile in VS Code

With `LaTeX Workshop`:
- open the main `.tex` file;
- run `LaTeX Workshop: View LaTeX PDF`;
- save the file to rebuild;
- the PDF refreshes after each successful compilation.

### 5. Version the generated project

Each generated project is standalone, so you can version it separately:

```bash
cd my-project
git init
git add .
git commit -m "Initial report"
```

Then create a dedicated GitHub repository for that project only.

Typical collaboration workflow:
- create the project with `latex-toolbox`;
- initialize Git inside the generated folder;
- create one private GitHub repository for that project;
- invite only the people who should access that document.

## Available templates

### `rapport-projet-en`

English project-report template with:
- cover page
- table of contents
- introduction
- conclusion
- AI statement

### `rapport-projet-fr`

Same structure as `rapport-projet-en`, but in French.

### `rapport-ter`

French academic TER-style report template with a more detailed structure.

### `research`

English research-style template with:
- cover page
- abstract
- table of contents
- two-column main body
- introduction
- conclusion
- appendix
- AI usage note
- BibTeX bibliography

## Generated project structure

Typical structure:

```text
my-project/
├── my-project.tex
├── frontmatter/
├── sections/
├── backmatter/ or appendix/
├── references/ or bibliography/
├── figures/
├── images/
├── screens/
├── assets/
│   ├── images/common/
│   └── logos/
└── styles/packages/
```

Important points:
- the main file uses the project name;
- LaTeX styles are copied into the project;
- logos are copied into the project;
- the project can be shared without shipping the whole toolbox repository.

## Modular styles

The source styles live in:

```text
styles/packages/
```

Main files:
- `university-project-report.sty`
- `university-ter-report.sty`
- `research-article.sty`
- `report-metadata.sty`
- `report-tables.sty`
- `report-code-python.sty`
- `report-code-bash.sty`
- `report-colors.sty`
- `report-ter-titlepage.sty`
- `report-theorems-fr.sty`

When a project is created, these styles are copied into the generated project under:

```text
styles/packages/
```

## Assets and logos

The repository-level folder:

```text
assets/logos/
```

is used as the source for logos copied into new projects.

In a generated project:
- place logos in `assets/logos/`
- place reusable images in `assets/images/common/`

## Bibliography

The `research` template uses a separate BibTeX file.

Typical path:

```text
references/references.bib
```

Add your references there and compile the document normally.

## VS Code snippets

Snippets are provided in:

```text
.vscode/latex.code-snippets
```

Useful snippet prefixes:
- `ltx-code-py`
- `ltx-code-sh`
- `ltx-fig`
- `ltx-screen`
- `ltx-ai`
- `ltx-toc`

## Evolving the toolbox

If you update:
- templates in `templates/`
- styles in `styles/packages/`
- logos in `assets/logos/`

then future generated projects will include those changes.

Already-generated projects are not updated automatically, because they embed their own local copies.

## Repository structure

```text
LaTeX/
├── assets/
├── latex_toolbox/
├── projects/
├── scripts/
├── styles/
├── templates/
└── .vscode/
```

Role of each folder:
- `latex_toolbox/`: Python code for the CLI
- `templates/`: source templates
- `styles/`: shared toolbox styles
- `assets/`: shared logos and reusable resources
- `projects/`: optional place to keep real generated projects
- `scripts/`: compatibility wrappers

## Quick command reference

List templates:

```bash
latex-toolbox list-templates
```

Create an English project report:

```bash
latex-toolbox create --name my-project --template rapport-projet-en
```

Create a French project report:

```bash
latex-toolbox create --name mon-projet --template rapport-projet-fr
```

Create a research project:

```bash
latex-toolbox create --name paper-audio-search --template research
```

## Summary

LaTeX Toolbox helps you:
- create LaTeX projects quickly;
- reuse your styles and logos;
- work comfortably in VS Code;
- share each generated project as its own Git repository.
