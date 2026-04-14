---
name: migrate-from-mypy
description: "Migrate type checking from mypy to ty. Use when the user wants to switch from mypy to ty, try ty, compare mypy and ty output, or set up ty alongside mypy."
---

# Migrate from mypy to ty

Incrementally adopt ty as a type checker alongside or instead of mypy. This migration adds ty first, runs both checkers in parallel, and only removes mypy when the user is confident in the switch.

## Workflow

### 1. Assess the current mypy setup

Find the mypy configuration. Check these locations in order:

- `pyproject.toml` under `[tool.mypy]`
- `mypy.ini`
- `setup.cfg` under `[mypy]`
- `.mypy.ini`

Report to the user:

- **Strictness level**: Is `strict = true` enabled, or are individual strict flags set?
- **Ignored errors**: Any `# type: ignore` comments, `disable_error_code` settings, or per-module `ignore_errors = true`.
- **Per-module overrides**: Any `[[tool.mypy.overrides]]` or `[mypy-module.*]` sections.
- **Plugins**: Any mypy plugins in use (e.g., `plugins = ["pydantic.mypy", "sqlalchemy.ext.mypy.plugin"]`). Note that ty does not support mypy plugins; some of these may not be needed since ty handles certain patterns natively.

### 2. Establish the mypy baseline

Run mypy using the project's existing command:

```bash
uv run mypy .
```

Or whatever command the project uses (check CI config, Makefile, or scripts). Record:

- Total error count
- Categories of errors (e.g., `[assignment]`, `[arg-type]`, `[return-value]`)
- Whether the run passes or fails in CI

### 3. Run ty for the first time

ty does not need to be installed. Run it with uvx:

```bash
uvx ty check
```

Record the error count and note differences from mypy. ty is a different type checker with different defaults and different diagnostic names, so the outputs will not match one-to-one.

### 4. Compare the two outputs

Summarize the differences for the user:

- **Errors only mypy found**: These may be real issues ty does not yet check for, or mypy-specific diagnostics.
- **Errors only ty found**: ty may catch issues mypy misses, particularly around control flow and type narrowing.
- **Shared findings**: Errors both tools report, possibly with different messages or severity.

Frame this as informational. The goal is awareness, not immediate action on every discrepancy.

### 5. Configure ty

Add a `[tool.ty]` section to `pyproject.toml`. Map relevant mypy settings where equivalents exist:

```toml
[tool.ty]
respect-ignore-comments = true
```

Common mypy-to-ty mappings:

| mypy setting | ty equivalent | Notes |
|---|---|---|
| `python_version` | `python-version` | Same format (e.g., "3.12") |
| `strict = true` | No single flag | ty's defaults are stricter than mypy's non-strict mode |
| `ignore_missing_imports` | `unresolved-import = "ignore"` under `[tool.ty.rules]` | Suppress import errors |
| `disable_error_code` | `[tool.ty.rules]` with specific rule names | Rule names differ between tools |
| `exclude` | `exclude` | Glob patterns to skip |

Settings with no ty equivalent yet: mypy plugins, `incremental`, `cache_dir`, `show_error_codes` (ty always shows codes), `warn_unused_ignores`. Note these for the user.

### 6. Set up parallel running in CI

Recommend keeping both checkers during the transition. Example CI configuration:

```yaml
# In your CI workflow
- run: uv run mypy .
- run: uvx ty check
```

If ty produces errors the team is not ready to fix, configure ty to warn instead of error on those specific rules so CI still passes:

```toml
[tool.ty.rules]
# Example: downgrade specific rules to warnings during transition
possibly-unbound = "warn"
```

### 7. Iterate on ty configuration

As the team addresses ty findings:

- Fix type errors that both tools agree on first.
- Gradually tighten ty rules from `"warn"` to `"error"`.
- Add `# ty: ignore[rule-name]` comments for intentional suppressions.

### 8. Cut over to ty only

**Only proceed when the user is ready.** Do not remove mypy without explicit confirmation.

When the user decides to switch:

```bash
uv remove mypy
```

Remove the mypy configuration:

- Delete `[tool.mypy]` and `[[tool.mypy.overrides]]` from `pyproject.toml`
- Delete `mypy.ini` or `.mypy.ini` if they exist
- Remove `[mypy]` and `[mypy-*]` sections from `setup.cfg` if present

Update CI configuration to replace `uv run mypy .` with `uvx ty check` (or `uv run ty check` if ty is a dev dependency).

Search the codebase for `# type: ignore` comments. These still work in ty, but ty's comment syntax is `# ty: ignore[rule-name]`. Offer to convert specific ones where the rule name is known.

## Learn more

- [How to migrate from mypy to ty](https://pydevtools.com/handbook/how-to/how-to-migrate-from-mypy-to-ty/)
- [How to try the ty type checker](https://pydevtools.com/handbook/how-to/how-to-try-the-ty-type-checker/)
- [How to gradually adopt type checking in an existing Python project](https://pydevtools.com/handbook/how-to/how-to-gradually-adopt-type-checking-in-an-existing-python-project/)
