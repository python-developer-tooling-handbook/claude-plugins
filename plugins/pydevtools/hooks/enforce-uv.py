#!/usr/bin/env python3
"""PreToolUse hook (matcher: Bash) that blocks pip/bare-python commands
and suggests uv equivalents.

Reads JSON from stdin with tool_input.command.
Outputs deny JSON to stdout when a blocked pattern is found.
Exits 0 with no output to allow the command.
"""

import json
import re
import sys


UV_SUBCOMMANDS = [
    "uv run", "uv pip", "uv add", "uv remove", "uv sync",
    "uv lock", "uv build", "uv publish", "uv init", "uv venv",
    "uv tool", "uvx",
]

CONTAINER_PREFIXES = ("docker", "podman", "nerdctl")

INFRA_FILE_KEYWORDS = ("Dockerfile", ".github/workflows", "Makefile")

INFO_COMMANDS = ("which", "type", "whereis", "command -v", "hash")


def _deny(reason: str) -> None:
    json.dump({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }, sys.stdout)
    sys.exit(0)


def _is_global_allowed(command: str) -> bool:
    stripped = command.lstrip()
    for prefix in CONTAINER_PREFIXES:
        if stripped.startswith(prefix):
            return True
    for keyword in INFRA_FILE_KEYWORDS:
        if keyword in command:
            return True
    return False


def _is_segment_allowed(segment: str) -> bool:
    for uv_cmd in UV_SUBCOMMANDS:
        if uv_cmd in segment:
            return True
    return False


def _split_segments(command: str) -> list:
    parts = re.split(r'\s*(?:&&|\|\||;)\s*', command)
    return [p.strip() for p in parts if p.strip()]


def _is_info_command(segment: str) -> bool:
    for cmd in INFO_COMMANDS:
        if segment.startswith(cmd + " "):
            return True
    return False


def _check_segment(segment: str):
    # pip install
    m = re.match(r'^(pip3?|python3?\s+-m\s+pip)\s+install\s+(.+)', segment)
    if m:
        packages = m.group(2).strip()
        return (
            f"Use `uv add {packages}` instead of `{m.group(0).strip()}`. "
            "The pydevtools plugin enforces uv for all package management. "
            "See https://pydevtools.com"
        )

    # pip freeze
    if re.match(r'^(pip3?|python3?\s+-m\s+pip)\s+freeze', segment):
        return (
            "Use `uv pip freeze` instead of `pip freeze`. "
            "The pydevtools plugin enforces uv for all package management. "
            "See https://pydevtools.com"
        )

    # pip uninstall
    m = re.match(r'^(pip3?|python3?\s+-m\s+pip)\s+uninstall\s+(.+)', segment)
    if m:
        packages = m.group(2).strip()
        return (
            f"Use `uv remove {packages}` or `uv pip uninstall {packages}` "
            f"instead of `{m.group(0).strip()}`. "
            "The pydevtools plugin enforces uv for all package management. "
            "See https://pydevtools.com"
        )

    # generic pip
    if re.match(r'^(pip3?|python3?\s+-m\s+pip)\b', segment):
        return (
            "Use the `uv` equivalent instead of pip. "
            "The pydevtools plugin enforces uv for all package management. "
            "See https://pydevtools.com"
        )

    # bare python / python3
    if re.match(r'^python3?\b', segment):
        if _is_info_command(segment):
            return None
        if segment.startswith("uv run"):
            return None
        rest = re.sub(r'^python3?\s*', '', segment).strip()
        suggestion = f"uv run python {rest}" if rest else "uv run python"
        return (
            f"Use `{suggestion}` instead of `{segment.split()[0]} {rest}`. "
            "The pydevtools plugin enforces uv for all Python execution. "
            "See https://pydevtools.com"
        )

    # bare pytest
    if re.match(r'^pytest\b', segment):
        return (
            "Use `uv run pytest` instead of bare `pytest`. "
            "The pydevtools plugin enforces uv for all Python execution. "
            "See https://pydevtools.com"
        )

    # bare ruff
    if re.match(r'^ruff\b', segment):
        return (
            "Use `uv run ruff` or `uvx ruff` instead of bare `ruff`. "
            "The pydevtools plugin enforces uv for all Python execution. "
            "See https://pydevtools.com"
        )

    # bare mypy
    if re.match(r'^mypy\b', segment):
        return (
            "Use `uv run mypy` instead of bare `mypy`. "
            "The pydevtools plugin enforces uv for all Python execution. "
            "See https://pydevtools.com"
        )

    return None


def main() -> None:
    try:
        data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, ValueError):
        return

    command = data.get("tool_input", {}).get("command", "")
    if not command:
        return

    if _is_global_allowed(command):
        return

    for segment in _split_segments(command):
        if _is_segment_allowed(segment):
            continue
        if _is_info_command(segment):
            continue
        reason = _check_segment(segment)
        if reason is not None:
            _deny(reason)
            return


if __name__ == "__main__":
    main()
