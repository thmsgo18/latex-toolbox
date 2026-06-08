# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [0.2.4] - 2026-06-08

### Added
- New built-in template `blank`: minimal pdfLaTeX `article` starter with title, author, and one section — the simplest possible starting point.
- `latex-forge template install` now raises an error if the template name is already installed, preventing silent overwrites. Add `--force` to overwrite explicitly.
- Attempting to install a template with the same name as a built-in template now raises a clear error.

### Fixed
- `AGENTS.md` and `GETTING_STARTED.md` now reflect the actual LaTeX engine of the template instead of always showing LuaLaTeX.
- Added `.claude/` to `.gitignore` so Claude Code session files are never accidentally committed.

## [0.2.3] - 2026-06-08

### Changed
- Renamed the built-in templates `rapport-projet-en`/`rapport-projet-fr` to `project-report-en`/`project-report-fr`, so the template name is in English regardless of the document's language — consistent with `cv-en`/`cv-fr`. Update `--template`, `default_template`, and any scripts that reference the old names.

## [0.2.2] - 2026-06-07

### Added
- Project creation now reads the LaTeX engine (`lualatex`/`xelatex`/`pdflatex`) from each template's `latexforge.toml` and generates the matching `latexmk` recipe in `.vscode/settings.json`
- `apply_profile_to_metadata` (now removed, see below) gained `\author{PLACEHOLDER}` recognition before the feature was dropped entirely

### Changed
- Both READMEs rewritten to lead with the live PDF preview experience rather than LaTeX itself, with a real screenshot and an "AI-friendly by design" section

### Removed
- The `latex-forge profile` command and the whole user-profile feature (`get_profile`/`save_profile`, `apply_profile_to_metadata`, `apply_profile_to_cv_heading`, the first-launch profile prompt, and related tests/docs). Generated projects now keep their template placeholders for the user to fill in directly.

## [0.2.0] - 2026-06-02

### Added
- Interactive mode: `create` prompts for name, template, and output directory when arguments are omitted
- `--output` flag to specify where the project is created
- `--version` flag
- Guided LaTeX installation: first run checks the environment and offers to install LaTeX automatically
- `latex-forge setup` now prompts interactively to install LaTeX when it is missing, without requiring `--install-tex`
- Offer to open the generated project in VS Code after creation
- Installation duration warning for long-running commands (MacTeX takes ~20-30 min)
- Name validation: rejects spaces, special characters, and dot-prefixed names
- 29 automated tests covering all critical paths
- PyPI metadata: authors, readme, keywords, classifiers, project URLs
- MIT license
- GitHub Actions workflow for automated PyPI publishing on version tags
- CI workflow running tests on Python 3.10, 3.11, and 3.12

### Changed
- All CLI messages translated to English
- `create_project` is now atomic: the project folder is removed automatically if an error occurs mid-creation
- `patch_local_style` now uses a regex instead of fragile exact-string matching
- `rename_project` and `rename_current_project` refactored into a shared `_rename` helper
- Templates, styles, and assets moved inside the Python package for correct pip distribution
- Cleaner output after `create`: removed internal technical details

### Fixed
- `sys.stdin.isatty()` inconsistency in interactive checks replaced with `_is_interactive()` helper
- `KeyboardInterrupt` during template selection now exits cleanly instead of looping
- `OSError` handling added to all prompt functions for robustness on Windows and in CI environments

### Removed
- Legacy `scripts/new-project.py` and `scripts/new-project.sh` compatibility wrappers

## [0.1.0] - 2026-06-01

### Added
- Initial release
- `create` command to generate standalone LaTeX projects from templates
- `rename` command to rename a project folder and its main `.tex` file
- `setup` command to check and install the LaTeX environment
- `list-templates` command
- Four templates: `rapport-projet-en`, `rapport-projet-fr`, `rapport-ter`, `research`
- Automatic style dependency resolution
- VS Code settings and extension recommendations generated per project
- Standalone setup scripts embedded in each generated project
- Cross-platform support: macOS, Linux, Windows
- Published to PyPI
