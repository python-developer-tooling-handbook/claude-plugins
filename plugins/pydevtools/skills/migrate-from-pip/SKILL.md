---
name: migrate-from-pip
description: "Migrate a Python project from requirements.txt to pyproject.toml with uv. Use when the user wants to convert from pip, migrate requirements.txt, switch from pip to uv, or modernize their Python project setup."
---

# Migrate from pip/requirements.txt to uv

Convert a project that uses requirements.txt files and pip into one managed by uv with pyproject.toml.

## Workflow

### 1. Inventory requirements files

Search the project root for all requirements-related files:

- `requirements.txt`
- `requirements-dev.txt`, `requirements-test.txt`, `requirements-ci.txt`
- `requirements-lock.txt`, `requirements.lock`
- `constraints.txt`
- Any other `requirements*.txt` variants

Report what was found, the number of dependencies in each file, and note any unusual entries (editable installs, index URLs, constraint references).

### 2. Scan for edge cases before importing

Read each requirements file and flag lines that need manual handling:

- **`-e .` or `-e ./path`**: Editable self-installs. Skip these; they are self-references that uv handles differently.
- **`--find-links` or `--extra-index-url` or `--index-url`**: These become `[[tool.uv.index]]` entries in pyproject.toml. Note them for step 6.
- **`-c constraints.txt`**: Constraints should become version bounds on the relevant dependencies. Note them for step 6.
- **Platform markers** (e.g., `pywin32; sys_platform == "win32"`): These carry over automatically through `uv add -r`. No action needed.

### 3. Create pyproject.toml if missing

If no `pyproject.toml` exists:

```bash
uv init --bare
```

Ask the user for the project name and a one-line description. Update the `[project]` table with their answers.

If `pyproject.toml` already exists (e.g., from a `setup.py`/`setup.cfg` migration), skip this step.

### 4. Import main dependencies

```bash
uv add -r requirements.txt
```

If the project uses a differently named main requirements file, adjust accordingly.

### 5. Import dev and test dependencies

For each extra requirements file, import into the dev dependency group:

```bash
uv add --dev -r requirements-dev.txt
uv add --dev -r requirements-test.txt
```

If the project uses finer-grained groups (e.g., separate `test` and `lint` groups), ask the user whether to consolidate into `dev` or create separate dependency groups:

```bash
uv add --group test -r requirements-test.txt
uv add --group lint -r requirements-lint.txt
```

### 6. Handle flagged edge cases

Apply the fixes identified in step 2:

**Custom indexes**: Add to pyproject.toml:

```toml
[[tool.uv.index]]
url = "https://custom.index.example.com/simple/"
```

**Constraints**: Convert constraint pinnings to version bounds on the corresponding dependencies. For example, if `constraints.txt` pins `numpy<2.0`, ensure the dependency reads `numpy>=1.24,<2.0` (or whatever lower bound is appropriate).

### 7. Verify the migration

Run `uv sync` and confirm it exits successfully:

```bash
uv sync
```

If it fails, read the error and fix the issue. Common problems:
- Conflicting version constraints between files
- Packages that were renamed or removed from PyPI
- Python version incompatibilities (check `requires-python` in pyproject.toml)

### 8. Compare installed packages

Run `uv pip list` and compare the output against the original requirements files. Check for:

- Missing packages that were in requirements.txt but not in pyproject.toml
- Version mismatches that could cause runtime issues

### 9. Clean up old files

**Stop and ask the user before deleting anything.** Offer to remove:

- `requirements*.txt` files
- `constraints.txt`
- `setup.py` (if present and now redundant)
- `setup.cfg` (if present and now redundant)
- `MANIFEST.in` (if present and now redundant)

Do not delete files unless the user explicitly confirms.

### 10. Post-migration recommendations

Offer to set up additional tooling:

- **Ruff** for linting and formatting: `uv add --dev ruff`
- **Pre-commit hooks** with Ruff integration
- **pytest** if not already present: `uv add --dev pytest`
- **CLAUDE.md** with the project's new uv-based commands

## Learn more

- [How to migrate from requirements.txt to pyproject.toml with uv](https://pydevtools.com/handbook/how-to/how-to-migrate-from-requirements-txt-to-pyproject-toml-with-uv/)
- [Create your first Python project](https://pydevtools.com/handbook/tutorial/create-your-first-python-project/)
