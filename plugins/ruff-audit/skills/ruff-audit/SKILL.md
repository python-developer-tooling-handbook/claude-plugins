---
name: ruff-audit
description: Audit a project's Ruff linter configuration and interactively recommend rules to add. Use when the user wants to expand their Ruff rule set, review which rules they're missing, adopt new lint categories, tighten their Ruff config, or asks "what Ruff rules should I enable." Also trigger when someone mentions they just set up Ruff and want to go beyond the defaults, or when they ask about Ruff best practices for an existing project.
---

# Ruff Rule Audit

Audit the project's Ruff config, identify high-value rules that aren't enabled, and walk the user through adopting them — modifying the config file at the end.

## Phase 1: Gather State

### 1A: Find and read the Ruff config

Check for config files in precedence order. The first one found is the active config:

1. `.ruff.toml`
2. `ruff.toml`
3. `pyproject.toml` (look under `[tool.ruff]` and `[tool.ruff.lint]`)

Extract and note:
- `select` (replaces defaults entirely) vs `extend-select` (adds to defaults)
- `ignore` and `extend-ignore`
- `per-file-ignores`
- `preview` (true/false/absent)
- `fixable` / `unfixable`
- `target-version` (Python version target)

Also check for narrow rule selections that should be full categories. Common example: `I001` (a single isort rule) instead of `I` (the full isort category). Flag these as gaps.

If no Ruff config exists at all, note that the project is running pure defaults (`E4`, `E7`, `E9`, `F` only) and proceed — this is the highest-value audit scenario.

### 1B: Run a trial with ALL rules

Both commands return JSON arrays. Each element has `code` (string), `name` (string), `count` (int), and `fixable` (bool).

**Important**: the `fixable` field in statistics output respects the project's `fixable` setting. If the project restricts `fixable` (e.g., `fixable = ["I001", "F"]`), every other rule shows `fixable: false` even when Ruff can fix it. To get the true fixability picture, override this:

```bash
ruff check --select ALL --statistics --output-format json --config 'lint.fixable = ["ALL"]' 2>/dev/null
```

Also run with the current config to see the baseline:

```bash
ruff check --statistics --output-format json 2>/dev/null
```

### 1C: Detect project type from dependencies

Read `pyproject.toml` dependencies (or `requirements.txt` / `setup.py` if that's what the project uses) and flag framework-specific rule categories:

| If you find... | Recommend category | Prefix |
|---|---|---|
| `django` | flake8-django | DJ |
| `pytest` (or `tests/` directory) | flake8-pytest-style | PT |
| `numpy` | NumPy-specific rules | NPY |
| `pandas` | Pandas-vet | PD |
| `pydantic` or `fastapi` | FastAPI-specific rules | FAST |
| `.pyi` files present | flake8-pyi | PYI |
| `airflow` | Airflow | AIR |
| `logging` heavy usage | flake8-logging | LOG |

## Phase 2: Analyze and Classify

### 2A: Aggregate violations by prefix

For each rule prefix not currently enabled, aggregate the `--select ALL --statistics` JSON data. Extract the prefix from each `code` (the leading uppercase letters, e.g., `UP` from `UP007`). Pylint rules split into sub-prefixes (`PLC`, `PLE`, `PLR`, `PLW`) — group them under `PL` for the recommendation but show sub-prefix detail in the full table.

For each prefix, sum:
- **Total violations** (`count` field)
- **Fixable violations** (where `fixable` is `true` — from the `fixable = ["ALL"]` override run)
- **Manual-only violations** (total minus fixable)

### 2B: Classify into tiers

| Tier | Criteria |
|---|---|
| Recommended | In the recommended starter set (E, F, UP, B, SIM, I) but not enabled |
| Project-specific | Matches a detected framework dependency |
| Free win | 0 violations, or 100% auto-fixable |
| Low effort | Fewer than 10 manual fixes needed |
| Worth discussing | 10-50 manual fixes |
| Major adoption | 50+ manual fixes |

A prefix can belong to multiple tiers (e.g., UP is both Recommended and Worth discussing). The tier label shown to the user should be the highest-priority one (Recommended > Project-specific > Free win > Low effort > Worth discussing > Major adoption).

### 2C: Find config issues

Check for and flag:
- **Restrictive `fixable`**: If `fixable` is set to anything other than `["ALL"]` (Ruff's default), flag this. Count how many violations are auto-fixable with unrestricted `fixable` vs the current setting.
- **Narrow rule selections**: Individual rules (like `I001`) instead of full category prefixes (like `I`). List what they'd gain by broadening.
- **Stale ignores**: Every rule in `ignore` or `extend-ignore` that has 0 violations in the `--select ALL` output. If there are no ignores, say "No ignore list — nothing to clean up."
- **Preview opportunities**: If `preview` is not enabled, count how many preview-only rules would be relevant.

## Phase 3: Present Report and Get Decisions

The goal is to give the user the full picture in one message, then collect decisions in one or two rounds — not page through categories one at a time.

### Step 1: Print the full report as text

Output a markdown report directly in the conversation. Structure:

```
## Ruff Audit: [project name]

**Current config**: [select/extend-select values] | fixable: [value] | target: [py version]
**Baseline violations**: [count] across [N] rules
**With ALL rules**: [count] violations across [N] categories

### Config Issues

[List any: restrictive fixable, narrow selections, stale ignores — or "None found."]

### Recommended Starter Set Gaps

| Prefix | Category | Violations | Fixable | Manual | Notes |
|--------|----------|-----------|---------|--------|-------|
| UP     | pyupgrade | 96 | 75 | 21 | Modernizes syntax for py312 |
| ...    | ...       |    |    |    |    |

### Project-Specific Categories

| Prefix | Category | Violations | Fixable | Manual | Why |
|--------|----------|-----------|---------|--------|-----|
| FAST   | FastAPI  | 23 | 23 | 0 | fastapi in dependencies |
| ...    | ...      |    |    |   |   |

### All Other Unenabled Categories

| Prefix | Category | Violations | Fixable | Manual | Tier |
|--------|----------|-----------|---------|--------|------|
| SIM    | simplify | 3 | 3 | 0 | Free win |
| COM    | trailing commas | 223 | 223 | 0 | Free win |
| ...    | ...      |   |   |   |   |
```

Sort each table section by tier priority (free wins first, then low effort, then worth discussing, then major adoption), and within a tier by violation count ascending.

### Step 2: Collect decisions (1-2 AskUserQuestion calls max)

After the report, ask the user to decide with at most two questions:

**Question 1** — Scope: which tiers to enable. Use AskUserQuestion with options like:
- "All recommended + project-specific + free wins (Recommended)" — the sensible default
- "All recommended + project-specific + free wins + low effort"
- "Everything except major adoption"
- (User can always type "Other" to cherry-pick)

**Question 2** (only if needed) — If the user picks a tier that includes "worth discussing" or "major adoption" categories, ask once about the strategy for high-violation categories:
- "Auto-fix what's possible, leave the rest as violations"
- "Use --add-noqa to suppress existing violations, enforce going forward"
- "Skip categories with 50+ manual fixes"

If the user chose "Other" and listed specific prefixes, skip Question 2.

**Config issues**: If there are config issues (restrictive `fixable`, narrow selections, stale ignores), include them as part of Question 1 as a separate multi-select or fold them into the recommended option description. Don't burn a separate question round on config hygiene.

## Phase 4: Apply Changes

After the user responds, apply everything in one batch:

### 4A: Update the config file

- If the project uses `select`, add new prefixes to that list. If it uses `extend-select`, add there. If neither exists, add `extend-select`.
- Broaden narrow selections if approved (e.g., `I001` → `I`).
- Update `fixable` if approved.
- Remove stale ignores if approved.
- Keep prefixes in alphabetical order within lists.
- Add a brief inline comment for each new prefix (e.g., `"UP", # pyupgrade`).

### 4B: Run auto-fix

```bash
ruff check --fix
```

This applies safe fixes for all newly enabled rules. Report how many violations were fixed and how many remain.

### 4C: Verify

Run `ruff check` once more to confirm the config is valid and show the final state.

## Phase 5: Final Summary

Print a before/after summary:

```
## Ruff Audit Complete

**Before**: select = ["E", "W", "F", "C901", "I001"] (5 entries)
**After**:  select = ["A", "B", "E", "ERA", "F", "FIX", "I", "N", "PLW", "RUF", "SIM", "SLF", "TID", "UP", "W"] (15 entries)
**fixable**: ["I001", "F"] → ["ALL"]

**Auto-fixed**: 164 violations
**Remaining**: 57 violations across 8 rules (run `ruff check` to see them)
**Config file**: pyproject.toml
```
