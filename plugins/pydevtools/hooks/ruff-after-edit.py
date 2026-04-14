#!/usr/bin/env python3
"""PostToolUse hook (matcher: Write|Edit|MultiEdit) that runs Ruff
format and lint-fix on edited Python files.

Best-effort: never blocks, always exits 0.
"""

import json
import os
import shutil
import subprocess
import sys


def main() -> None:
    try:
        data = json.loads(sys.stdin.read())
        file_path = data.get("tool_input", {}).get("file_path", "")

        if not file_path or not file_path.endswith(".py") or not os.path.isfile(file_path):
            return

        if not shutil.which("uv"):
            return

        subprocess.run(
            ["uv", "run", "ruff", "check", "--fix", "--quiet", file_path],
            capture_output=True,
            timeout=10,
        )
        subprocess.run(
            ["uv", "run", "ruff", "format", "--quiet", file_path],
            capture_output=True,
            timeout=10,
        )
    except Exception:
        pass


if __name__ == "__main__":
    main()
