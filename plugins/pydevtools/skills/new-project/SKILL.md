---
name: new-project
description: "Create a new Python project with uv. Use when the user wants to create, initialize, or scaffold a new Python project, application, or library."
---

# New Python Project

Scaffold a production-ready Python project using uv with linting, testing, and pre-commit hooks configured from the start.

## Workflow

### 1. Gather requirements

Ask the user two questions (skip any already answered):

- **Application or library?** An application is a standalone program (CLI tool, web service, script). A library is a reusable package others install from PyPI. Default to application if unclear.
- **Project name?** Use lowercase with hyphens. Validate it is a legal Python package name.

### 2. Initialize the project

For an application:

```bash
uv init <project-name>
```

For a library/package:

```bash
uv init --package <project-name>
```

### 3. Add dev dependencies

```bash
cd <project-name>
uv add --dev pytest ruff
```

### 4. Configure Ruff

Append to `pyproject.toml`:

```toml
[tool.ruff]
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM", "TCH"]
```

### 5. Configure pytest

Append to `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
```

### 6. Create the test directory

Create `tests/__init__.py` (empty file).

Create `tests/test_placeholder.py`:

```python
def test_placeholder():
    assert True
```

### 7. Set up pre-commit

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.6
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

Install the hooks:

```bash
uvx pre-commit install
```

### 8. Create CLAUDE.md

Create a `CLAUDE.md` in the project root with these instructions:

```markdown
## Project

<project-name>: <brief description from user or "A Python project.">

## Tooling

- Package manager: uv
- Linter/formatter: Ruff
- Test runner: pytest

## Commands

- Install dependencies: `uv sync`
- Run tests: `uv run pytest`
- Lint: `uv run ruff check .`
- Format: `uv run ruff format .`
- Add a dependency: `uv add <package>`
- Add a dev dependency: `uv add --dev <package>`
```

### 9. Verify the setup

Run both commands and confirm they exit cleanly:

```bash
uv run pytest
uv run ruff check .
```

If either fails, fix the issue before proceeding.

### 10. Offer to initialize git

Ask the user if they want a git repository. If yes:

```bash
git init
git add .
git commit -m "Initial project setup"
```

## Learn more

- [Create your first Python project](https://pydevtools.com/handbook/tutorial/create-your-first-python-project/)
- [Modern Python project setup guide for AI assistants](https://pydevtools.com/handbook/explanation/modern-python-project-setup-guide-for-ai-assistants/)
- [How to configure recommended Ruff defaults](https://pydevtools.com/handbook/how-to/how-to-configure-recommended-ruff-defaults/)
- [How to set up pre-commit hooks for a Python project](https://pydevtools.com/handbook/how-to/how-to-set-up-pre-commit-hooks-for-a-python-project/)
