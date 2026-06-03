# Contributing to LaTeX Toolbox

Thanks for your interest in contributing!

## Reporting a bug

Open an issue on GitHub and include:
- your OS and Python version
- the exact command you ran
- the full error message

## Setting up the development environment

```bash
git clone https://github.com/thmsgo18/latex-forge.git
cd latex-forge
pipx install --editable ".[dev]"
```

## Running the tests

```bash
pytest tests/ -v
```

All tests must pass before submitting a pull request.

## Adding a template

1. Create a new folder under `latex_forge/templates/your-template-name/`
2. Add a `main.tex` and the required subfolders
3. Make sure `latex-forge create --name test --template your-template-name` works
4. Add tests if needed

## Submitting a pull request

1. Fork the repository
2. Create a branch: `git checkout -b my-fix`
3. Make your changes and run the tests
4. Open a pull request against `main`

## Releasing a new version

Maintainers only:

1. Update `version` in `pyproject.toml`
2. Commit and tag: `git tag vX.Y.Z`
3. Push: `git push && git push --tags`

GitHub Actions will publish to PyPI automatically.
