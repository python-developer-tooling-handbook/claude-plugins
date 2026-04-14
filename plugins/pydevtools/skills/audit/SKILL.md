---
name: audit
description: "Audit a Python project's tooling health. Use when the user wants to check project health, audit tooling setup, or review what's missing from their Python project configuration."
---

# Audit Python Project Tooling

Inspect a Python project's configuration and report what is set up correctly, what is missing, and what should be upgraded.

## Checks

Run every check below against the current working directory. Collect results, then present a single report at the end.

### 1. Package manager

Look for these lock files (in priority order):

| File | Tool |
|---|---|
| `uv.lock` | uv |
| `poetry.lock` | Poetry |
| `pdm.lock` | PDM |
| `Pipfile.lock` | Pipenv |
| `requirements.txt` (alone) | pip |

Report which package manager is in use. If the project does not use uv, flag this as a recommendation.

### 2. pyproject.toml

Check if `pyproject.toml` exists.

If `setup.py` or `setup.cfg` exists instead (or alongside), flag them as outdated. Projects should use `pyproject.toml` as the single source of project metadata.

### 3. Linting and formatting (Ruff)

Check for Ruff configuration in any of: `[tool.ruff]` in pyproject.toml, `ruff.toml`, `.ruff.toml`.

If present, check whether both linting (`[tool.ruff.lint]` or `select`) and formatting (`line-length` or `[tool.ruff.format]`) are configured.

If Ruff is not configured, check for legacy tools: `[tool.flake8]`, `.flake8`, `[tool.black]`, `[tool.isort]`. Report these as replaceable by Ruff.

### 4. Type checking

Check for any of:
- `[tool.mypy]` in pyproject.toml or `mypy.ini`
- `[tool.pyright]` in pyproject.toml or `pyrightconfig.json`
- `[tool.ty]` in pyproject.toml

If no type checker is configured, spot-check 3-5 `.py` files (prefer files in `src/` or the main package directory). Look for type annotations in function signatures (`: ` followed by a type in `def` lines, or `->` return types). Report whether annotations exist but no checker is configured.

### 5. Testing

Check for:
- `[tool.pytest.ini_options]` in pyproject.toml, or `pytest.ini`, or `conftest.py`
- A `tests/` directory (or `test/`)

Report whether a test framework is configured and whether test files exist.

### 6. Pre-commit hooks

Check for `.pre-commit-config.yaml` or `.prek.toml`.

If present, check whether Ruff hooks are included. If pre-commit exists but uses flake8/black/isort hooks, recommend switching to Ruff.

### 7. Legacy artifacts

Flag any of these files if they exist alongside a `pyproject.toml`:

- `setup.py`
- `setup.cfg`
- `requirements.txt` or `requirements-*.txt`
- `tox.ini` (check if `tox-uv` is used; flag only if it is not)
- `MANIFEST.in`
- `Pipfile`

### 8. CLAUDE.md

Check if `CLAUDE.md` exists in the project root. If it does, check whether it contains Python-specific instructions (look for mentions of `uv`, `pytest`, `ruff`, or common project commands). If missing, recommend creating one.

## Output format

Present results as a checklist. Use this format:

```
## Project Tooling Audit

- [x] **Package manager**: uv (uv.lock found)
- [x] **pyproject.toml**: Present
- [ ] **Linting**: Not configured
  > Recommendation: Add Ruff. See: https://pydevtools.com/handbook/how-to/how-to-configure-recommended-ruff-defaults/
- [!] **Type checking**: Annotations found in 3/5 files but no checker configured
  > Recommendation: Add ty or mypy. See: https://pydevtools.com/handbook/how-to/how-to-gradually-adopt-type-checking-in-an-existing-python-project/
...
```

Use `[x]` for pass, `[ ]` for missing/fail, `[!]` for warning (partially configured or using a legacy tool).

## Recommendation links

Include the relevant link with each finding:

| Finding | Link |
|---|---|
| Not using uv | https://pydevtools.com/handbook/how-to/how-to-migrate-from-poetry-to-uv/ or https://pydevtools.com/handbook/how-to/how-to-migrate-from-requirements-txt-to-pyproject-toml-with-uv/ |
| No Ruff config | https://pydevtools.com/handbook/how-to/how-to-configure-recommended-ruff-defaults/ |
| No type checker | https://pydevtools.com/handbook/how-to/how-to-gradually-adopt-type-checking-in-an-existing-python-project/ |
| No pre-commit | https://pydevtools.com/handbook/how-to/how-to-set-up-pre-commit-hooks-for-a-python-project/ |
| Legacy setup.py/setup.cfg | https://pydevtools.com/handbook/how-to/how-to-migrate-from-requirements-txt-to-pyproject-toml-with-uv/ |
| No CLAUDE.md | https://pydevtools.com/handbook/explanation/modern-python-project-setup-guide-for-ai-assistants/ |

After presenting the report, ask the user if they want help fixing any of the findings.

## Learn more

- [How to migrate from Poetry to uv](https://pydevtools.com/handbook/how-to/how-to-migrate-from-poetry-to-uv/)
- [How to migrate from requirements.txt to pyproject.toml with uv](https://pydevtools.com/handbook/how-to/how-to-migrate-from-requirements-txt-to-pyproject-toml-with-uv/)
- [How to configure recommended Ruff defaults](https://pydevtools.com/handbook/how-to/how-to-configure-recommended-ruff-defaults/)
- [How to gradually adopt type checking in an existing Python project](https://pydevtools.com/handbook/how-to/how-to-gradually-adopt-type-checking-in-an-existing-python-project/)
- [How to set up pre-commit hooks for a Python project](https://pydevtools.com/handbook/how-to/how-to-set-up-pre-commit-hooks-for-a-python-project/)
