---
name: publish
description: "Publish a Python package to PyPI. Use when the user wants to publish to PyPI, release a package, build Python distributions, set up trusted publishing, or prepare a package for distribution."
---

# Publish a Python Package to PyPI

Guide a user through building, testing, and publishing a Python package to PyPI using uv.

## Workflow

### 1. Check prerequisites

Read `pyproject.toml` and verify the following are present:

**Required `[project]` fields**: `name`, `version`, `description`, `requires-python`

**Recommended `[project]` fields**: `license`, `authors`, `readme`, `classifiers`, `urls`

**Build system**: `[build-system]` must be configured. If missing, add hatchling as the default:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

Report any missing fields to the user and help them fill in the gaps before proceeding.

### 2. Verify package name availability

Ask the user to check whether the name is available on PyPI:

```
https://pypi.org/project/<package-name>/
```

If the name is taken, suggest alternatives (e.g., adding a prefix or choosing a more specific name). Do not proceed until the user confirms a name.

### 3. Build the package

```bash
uv build
```

Verify that both distribution formats were created in `dist/`:

- `dist/<name>-<version>.tar.gz` (source distribution)
- `dist/<name>-<version>-py3-none-any.whl` (wheel)

If the build fails, read the error and fix it. Common causes: missing `[build-system]`, import errors, missing `__init__.py`, or a README path that does not exist.

### 4. Test on TestPyPI first

Publish to TestPyPI to verify everything works without affecting the real index:

```bash
uv publish --publish-url https://test.pypi.org/legacy/
```

This will prompt for TestPyPI credentials. The user needs a TestPyPI account (separate from PyPI) at https://test.pypi.org/account/register/.

Verify the test upload by installing from TestPyPI:

```bash
uv pip install --index-url https://test.pypi.org/simple/ <package-name>
```

If the package has dependencies not on TestPyPI, add `--extra-index-url https://pypi.org/simple/` to the install command.

### 5. Publish to PyPI

Once TestPyPI works, publish to the real index:

```bash
uv publish
```

This will prompt for PyPI credentials (API token or username/password). The user needs a PyPI account at https://pypi.org/account/register/.

**Stop and confirm with the user before running this command.** Publishing to PyPI is not reversible: a version, once uploaded, cannot be re-uploaded even if deleted.

### 6. Post-publish verification

Install the package from PyPI to confirm it works:

```bash
uv pip install <package-name>
```

Run a quick import check:

```bash
uv run python -c "import <package_module>; print(<package_module>.__version__)"
```

### 7. Set up trusted publishing (recommended for future releases)

Trusted publishing lets GitHub Actions publish to PyPI without API tokens using OpenID Connect. This is more secure than storing tokens in repository secrets.

Ask the user if they want to set this up. If yes, they need to configure a publisher at `https://pypi.org/manage/project/<package-name>/settings/publishing/`. Then offer to create a GitHub Actions workflow for tag-based publishing:

```yaml
name: Publish to PyPI

on:
  push:
    tags:
      - "v*"

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv build
      - run: uv publish --trusted-publishing always
```

This workflow builds and publishes automatically when a version tag (e.g., `v0.1.0`) is pushed.

Point the user to the handbook guide for the full trusted publishing setup, including attestations.

## Learn more

- [Publishing your first Python package to PyPI](https://pydevtools.com/handbook/tutorial/publishing-your-first-python-package-to-pypi/)
- [How to publish to PyPI with trusted publishing](https://pydevtools.com/handbook/how-to/how-to-publish-to-pypi-with-trusted-publishing/)
- [How to publish Python packages with digital attestations](https://pydevtools.com/handbook/how-to/how-to-publish-python-packages-with-digital-attestations/)
