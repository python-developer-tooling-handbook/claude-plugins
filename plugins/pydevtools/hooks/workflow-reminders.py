#!/usr/bin/env python3
"""UserPromptSubmit hook (no matcher) that returns contextual reminders
based on keywords in the user's prompt.

Reads JSON from stdin with a `prompt` field.
Outputs additionalContext JSON when keywords match, otherwise exits silently.
"""

import json
import re
import sys

KEYWORD_RULES = [
    (
        re.compile(r"\b(install|add\s+package|add\s+dep)", re.IGNORECASE),
        "Use `uv add <package>` to add dependencies, not pip install.",
    ),
    (
        re.compile(r"\b(tests?|testing|pytest)\b", re.IGNORECASE),
        "Run tests with `uv run pytest`.",
    ),
    (
        re.compile(r"\b(formatt?(?:ing)?|lint(?:ing)?)\b", re.IGNORECASE),
        "Format: `uv run ruff format .` | Lint: `uv run ruff check --fix .`",
    ),
    (
        re.compile(r"\b(type\s*check|mypy|(?<!\w)ty(?!\w))\b", re.IGNORECASE),
        "Type-check with `uv run ty check` or `uv run mypy .`",
    ),
    (
        re.compile(r"\b(publish(?:ing)?|pypi|deploy(?:ing)?)\b", re.IGNORECASE),
        "Build and publish: `uv build && uv publish`. "
        "See https://pydevtools.com/handbook/tutorial/publishing-your-first-python-package-to-pypi/",
    ),
    (
        re.compile(r"\b(pre-commit|prek)\b", re.IGNORECASE),
        "Run hooks: `uvx pre-commit run --all-files`",
    ),
]


def main() -> None:
    try:
        data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, ValueError):
        return

    prompt = data.get("prompt", "")
    if not prompt:
        return

    reminders = []
    for pattern, reminder in KEYWORD_RULES:
        if pattern.search(prompt):
            reminders.append(reminder)

    if not reminders:
        return

    bullet_list = "\n".join(f"- {r}" for r in reminders)
    context = f"pydevtools reminders:\n{bullet_list}"

    json.dump({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
    }, sys.stdout)


if __name__ == "__main__":
    main()
