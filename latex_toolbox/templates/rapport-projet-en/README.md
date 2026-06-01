# Project Report Template

This project was generated from the `rapport-projet-en` template of LaTeX Toolbox.

It is designed for course reports, lab reports, collaborative class projects, and other structured academic documents written in English.

## What is included

This project already contains:
- a cover page
- a table of contents
- an introduction
- a conclusion
- an AI statement
- local LaTeX styles in `styles/packages/`
- local logos in `assets/logos/`
- VS Code settings in `.vscode/settings.json`
- a LaTeX-oriented `.gitignore`

The project is standalone: you can share only this folder and compile it without the full toolbox repository.

## Quick start

1. Run the local setup script.

macOS / Linux:

```bash
./scripts/setup.sh
```

Windows:

```bat
scripts\setup.bat
```

Any platform with Python:

```bash
python3 scripts/setup.py
```

If you want the script to also try installing the TeX distribution itself:

```bash
python3 scripts/setup.py --install-tex
```

The setup script:
- installs the recommended VS Code extensions when possible
- checks whether LaTeX tools are already installed
- tells you what to install depending on your operating system

2. Open this folder in VS Code.
3. Open the main file:

```text
./YOUR_PROJECT_NAME.tex
```

4. Edit:
- `frontmatter/metadata.tex`
- `sections/introduction.tex`
- `sections/conclusion.tex`
- `backmatter/ai-statement.tex`

5. Compile with `LaTeX Workshop`.

## What needs to be installed

To work comfortably on this project, each collaborator needs:
- VS Code
- the `LaTeX Workshop` extension
- a LaTeX distribution installed on the machine

Tip:
- start by running `scripts/setup.py` or `scripts/setup.sh`

Recommended VS Code extensions:
- `LaTeX Workshop`
- `LTeX+`
- `Code Spell Checker`

Important:
- if you use `LaTeX Workshop`, disable `vscode-pdf` to avoid PDF viewer conflicts

## Installation by operating system

### macOS

Recommended:
- install `MacTeX`

Why:
- it includes the standard LaTeX tools usually needed by academic projects
- it works well with `LaTeX Workshop`

After installation:
- restart VS Code
- check in a terminal:

```bash
latexmk --version
lualatex --version
```

### Windows

Recommended options:
- `TeX Live`
- or `MiKTeX`

If you want the most predictable setup across collaborators, prefer `TeX Live`.

If you want a lighter install with on-demand packages, `MiKTeX` is also a valid option.

After installation:
- restart VS Code
- check in PowerShell or Command Prompt:

```powershell
latexmk --version
lualatex --version
```

### Linux

Recommended:
- `TeX Live`

Common ways to install it:
- through your distribution package manager
- or through the official TeX Live installer

After installation:
- restart VS Code
- check in a terminal:

```bash
latexmk --version
lualatex --version
```

## First compilation in VS Code

1. Open the main `.tex` file.
2. Run:

```text
LaTeX Workshop: View LaTeX PDF
```

3. Save the file to trigger recompilation.

This project is configured so that:
- compilation runs on save
- generated build files go into `build/`
- the PDF opens in a VS Code tab

## If compilation fails

Typical causes:

1. `latexmk` or `lualatex` is not installed
- install a LaTeX distribution correctly

2. A package is missing
- with `TeX Live`, install the missing package with `tlmgr`
- with `MiKTeX`, allow automatic package installation or install it manually

3. VS Code does not see the LaTeX tools yet
- restart VS Code
- sometimes restarting the terminal or the machine helps too

## Project structure

```text
.
├── YOUR_PROJECT_NAME.tex
├── frontmatter/
├── sections/
├── backmatter/
├── figures/
├── images/
├── screens/
├── assets/
│   ├── images/common/
│   └── logos/
├── styles/packages/
├── .vscode/settings.json
└── .gitignore
```

## Where to edit things

Edit metadata here:

```text
frontmatter/metadata.tex
```

Edit the main content here:

```text
sections/
```

Put reusable images here:

```text
assets/images/common/
```

Put logos here:

```text
assets/logos/
```

## Collaboration

This project is designed to be shared as its own Git repository.

Typical workflow:

```bash
git init
git add .
git commit -m "Initial report"
```

Then push it to GitHub and invite only the collaborators who need access to this report.

If you want to create a private GitHub repository from this project with the GitHub CLI:

```bash
gh auth login
git init
git add .
git commit -m "Initial report"
git branch -M main
gh repo create your-project-name --private --source=. --remote=origin --push
```

Replace `your-project-name` with the repository name you want on GitHub.

## Useful official references

- VS Code LaTeX extension: LaTeX Workshop
- TeX distributions:
  - macOS: MacTeX
  - cross-platform: TeX Live
  - Windows/macOS/Linux: MiKTeX
