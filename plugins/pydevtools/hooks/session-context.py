#!/usr/bin/env python3
"""SessionStart hook that provides static best-practice context and a
lightweight project-health scan.

Reads JSON from stdin (uses `cwd` for file-existence checks).
Outputs additionalContext JSON to stdout.
"""

import json
import os
import sys

BEST_PRACTICES = (
    "Python best practices (pydevtools.com): "
    "Use uv for all package management (uv add, uv run, uv sync). "
    "Lint and format with `uv run ruff`. "
    "Type-check with `uv run ty check`. "
    "Test with `uv run pytest`. "
    "All config belongs in pyproject.toml. "
    "Never use pip directly. "
    "Full guide: https://pydevtools.com/handbook/explanation/modern-python-project-setup-guide-for-ai-assistants/"
)

MAX_FINDINGS = 3


def _scan_project(cwd):
    findings = []

    pyproject_path = os.path.join(cwd, "pyproject.toml")
    has_pyproject = os.path.isfile(pyproject_path)

    if not has_pyproject:
        findings.append(
            "No pyproject.toml found. Run `uv init` to create one."
        )
    else:
        ruff_configured = False
        try:
            with open(pyproject_path, "r", encoding="utf-8") as f:
                content = f.read()
            if "[tool.ruff]" in content:
                ruff_configured = True
        except OSError:
            pass

        if not ruff_configured and not os.path.isfile(os.path.join(cwd, "ruff.toml")):
            findings.append(
                "Ruff not configured in pyproject.toml. "
                "See https://pydevtools.com/handbook/how-to/how-to-configure-recommended-ruff-defaults/"
            )

        if os.path.isfile(os.path.join(cwd, "requirements.txt")):
            findings.append(
                "Found requirements.txt alongside pyproject.toml. "
                "Consider migrating: https://pydevtools.com/handbook/how-to/how-to-migrate-from-requirements-txt-to-pyproject-toml-with-uv/"
            )

        if not os.path.isfile(os.path.join(cwd, "uv.lock")):
            findings.append(
                "No uv.lock found. Run `uv lock` to create one."
            )

    has_precommit = os.path.isfile(os.path.join(cwd, ".pre-commit-config.yaml"))
    has_prek = os.path.isfile(os.path.join(cwd, ".prek.toml"))
    if not has_precommit and not has_prek:
        findings.append(
            "No pre-commit config found. "
            "See https://pydevtools.com/handbook/how-to/how-to-set-up-pre-commit-hooks-for-a-python-project/"
        )

    return findings[:MAX_FINDINGS]


def main() -> None:
    try:
        data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, ValueError):
        data = {}

    cwd = data.get("cwd", os.getcwd())

    findings = _scan_project(cwd)

    if findings:
        findings_text = " ".join(findings)
        context = f"{BEST_PRACTICES} Project health: {findings_text}"
    else:
        context = BEST_PRACTICES

    json.dump({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }, sys.stdout)


if __name__ == "__main__":
    main()
