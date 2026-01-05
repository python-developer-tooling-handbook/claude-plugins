---
name: new-python-project
description: Set up a new Python project/folder/repo to build a cli, app, package, or other project
---

# Python Project Setup Skill

This skill helps set up Python projects using modern tooling. Use it for:
- Creating new projects from scratch
- Adding Python tooling to existing directories
- Converting legacy projects to modern standards
- Setting up specific components (just testing, just linting, etc.)

## First: Understand the Situation

Use AskUserQuestion to clarify what's needed. Adapt questions to context:

- **Starting fresh or existing code?** - Determines if we use `uv init` or add tooling to what's there
- **Package or application?** - Packages are imported by others (`uv init --package`), apps are run directly (`uv init`)
- **What's the scope?** - Full setup? Just add pytest? Just configure ruff? Add a CLI?
- **Any constraints?** - Python version, specific dependencies, org standards, existing CI

Don't ask unnecessary questions - if user says "set up a CLI tool called foo", you already know: it's new, it's a package, it needs a CLI entry point.

## Core Tooling

Use `uv` for everything Python:

| Task | Command |
|------|---------|
| New package | `uv init --package <name>` |
| New application | `uv init <name>` |
| Add dependency | `uv add <package>` |
| Add dev dependency | `uv add --dev <package>` |
| Run in environment | `uv run <command>` |
| One-off tool | `uvx <tool>` |

Standard dev dependencies: `uv add --dev pytest pytest-cov ruff pre-commit`

## Configurations

### pytest (pyproject.toml)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=src --cov-report=term-missing"
```

### ruff (pyproject.toml)

```toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM", "PTH"]
ignore = ["E501"]

[tool.ruff.format]
quote-style = "double"
```

### pre-commit (.pre-commit-config.yaml)

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.6
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
```

Install with: `uv run pre-commit install`

### CLI entry point (pyproject.toml)

```toml
[project.scripts]
<command-name> = "<package_name>.main:main"
```

### Type checking with mypy (pyproject.toml)

```toml
[tool.mypy]
python_version = "3.12"
strict = true
```

Add with: `uv add --dev mypy`

## Project Structures

**Package** (importable library or CLI tool):
```
<project>/
├── src/<package_name>/
│   ├── __init__.py
│   └── ...
├── tests/
├── pyproject.toml
└── ...
```

**Application** (scripts, services, one-off tools):
```
<project>/
├── src/
│   └── main.py (or multiple modules)
├── tests/
├── pyproject.toml
└── ...
```

These are starting points - adapt to what makes sense.

## Common Scenarios

**"Add testing to my existing project"**
- `uv add --dev pytest pytest-cov`
- Add pytest config to pyproject.toml
- Create tests/ directory with initial test file

**"Set up linting and formatting"**
- `uv add --dev ruff pre-commit`
- Add ruff config to pyproject.toml
- Create .pre-commit-config.yaml
- `uv run pre-commit install`

**"Convert this to a proper package"**
- Restructure into src/<package_name>/
- Add `[build-system]` and `[project]` to pyproject.toml
- Add `[project.scripts]` if CLI needed

**"Quick script project, minimal setup"**
- `uv init <name>` and that's it
- Add dependencies as needed with `uv add`

**"Production-ready library"**
- Full package structure with src layout
- pytest + coverage + mypy + ruff + pre-commit
- py.typed marker for type hints
- Comprehensive pyproject.toml metadata

## Reference

Run tests: `uv run pytest`
Lint: `uv run ruff check .`
Format: `uv run ruff format .`
Type check: `uv run mypy src`
Run script: `uv run python src/main.py`
Run CLI: `uv run <command-name>`

Lock files: Commit `uv.lock` for applications (reproducibility), optional for libraries.
