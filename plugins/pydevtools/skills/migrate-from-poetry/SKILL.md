---
name: migrate-from-poetry
description: "Migrate a Python project from Poetry to uv. Use when the user wants to switch from Poetry to uv, convert poetry.lock, or move their Poetry project to uv."
---

# Migrate from Poetry to uv

Guide the user through converting a Poetry-managed Python project to uv. This is a multi-step process with destructive operations. Confirm before deleting any files or removing any configuration.

## Workflow

### 1. Verify prerequisites

Check all three conditions before proceeding:

- `pyproject.toml` exists and contains `[tool.poetry]` sections
- `poetry.lock` exists
- `uv` is available (`uv --version`)

If any check fails, stop and explain what is missing.

### 2. Run the automated migration

```bash
uvx migrate-to-uv
```

This tool handles the bulk of the conversion: it rewrites `pyproject.toml` to use PEP 621 metadata, converts dependency specifications, and generates `uv.lock`.

Read through the output. If the tool reports errors or warnings, address them before continuing.

### 3. Verify the migration

```bash
uv sync
```

This must succeed without errors. If it fails, read the error output and fix dependency issues in `pyproject.toml` before retrying.

### 4. Compare resolved versions

Run `uv pip list` and compare key packages against what was in `poetry.lock`. Focus on:

- Major version differences in core dependencies
- Missing packages that were in the Poetry lock file
- Unexpected new transitive dependencies

Report any significant drift to the user.

### 5. Check for features that need manual attention

The automated tool does not handle every Poetry feature. Inspect `pyproject.toml` for each of these:

**Custom source repositories**

If the Poetry config had `[[tool.poetry.source]]` entries, these need manual conversion to `[tool.uv.index]` entries in `pyproject.toml`. Example:

```toml
# Poetry (old)
[[tool.poetry.source]]
name = "private"
url = "https://pypi.example.com/simple/"

# uv (new)
[[tool.uv.index]]
name = "private"
url = "https://pypi.example.com/simple/"
```

**Scripts and plugins**

`[tool.poetry.scripts]` should be converted to `[project.scripts]`. `[tool.poetry.plugins]` should be converted to `[project.entry-points]`. Check if `migrate-to-uv` handled these; fix manually if not.

**Build system**

Verify that `[build-system]` is set to a PEP 517 backend (hatchling is the default for `migrate-to-uv`). It should not reference `poetry-core` anymore.

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**Poetry extras**

`[tool.poetry.extras]` should be converted to `[project.optional-dependencies]`. Verify the conversion is correct.

### 6. Run the test suite

```bash
uv run pytest
```

If tests fail, investigate whether the failures are related to the migration (dependency version changes, import path changes) or pre-existing.

### 7. Clean up

Ask the user before each of these steps. Do not proceed without confirmation.

**Remove poetry.lock:**

```bash
rm poetry.lock
```

**Remove leftover Poetry sections from pyproject.toml:**

Check for and remove any remaining `[tool.poetry]`, `[tool.poetry.dependencies]`, `[tool.poetry.group.*]`, `[tool.poetry.scripts]`, `[tool.poetry.plugins]`, or `[tool.poetry.source]` sections.

**Optionally uninstall Poetry:**

```bash
pipx uninstall poetry
```

Only suggest this if the user has no other projects using Poetry.

### 8. Post-migration setup

After the migration is complete, offer to set up these if they are not already configured:

- **Ruff**: Add `[tool.ruff]` configuration if not present. See the new-project skill for defaults.
- **Pre-commit**: Create or update `.pre-commit-config.yaml` with Ruff hooks.
- **CLAUDE.md**: Create or update with uv-based commands.

### 9. Final verification

Run the full check:

```bash
uv sync && uv run pytest && uv run ruff check .
```

All three commands must pass. Report the final status to the user.

## Learn more

- [How to migrate from Poetry to uv](https://pydevtools.com/handbook/how-to/how-to-migrate-from-poetry-to-uv/)
- [How to configure recommended Ruff defaults](https://pydevtools.com/handbook/how-to/how-to-configure-recommended-ruff-defaults/)
