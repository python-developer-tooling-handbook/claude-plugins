# Claude Code Skill: New Python Project

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill for setting up Python projects with modern tooling.

Part of the [Python Developer Tooling Handbook](https://github.com/python-developer-tooling-handbook).

## What This Skill Does

This skill helps Claude Code set up Python projects using best practices:

- **uv** for package and environment management
- **pytest** for testing with coverage
- **ruff** for linting and formatting
- **pre-commit** for automated code quality
- **mypy** for type checking (optional)

It handles new projects, adding tooling to existing code, and converting legacy projects.

## Installation

Add this skill to your Claude Code configuration:

```bash
# Global installation (available in all projects)
claude mcp add-skill --global python-developer-tooling-handbook/claude-skill-new-python-project

# Or per-project
claude mcp add-skill python-developer-tooling-handbook/claude-skill-new-python-project
```

Alternatively, add to your `.claude/settings.json`:

```json
{
  "skills": [
    "python-developer-tooling-handbook/claude-skill-new-python-project"
  ]
}
```

## Usage

Once installed, ask Claude Code things like:

- "Set up a new Python project called my-tool"
- "Create a CLI package named mycli"
- "Add pytest and ruff to this project"
- "Convert this to a proper Python package"
- "Set up pre-commit hooks"

The skill will guide Claude to ask clarifying questions and apply the appropriate tooling.

## Requirements

- [uv](https://docs.astral.sh/uv/) must be installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

## Learn More

- [Python Developer Tooling Handbook](https://pythontooling.com) - Comprehensive guide to modern Python tooling
- [uv Documentation](https://docs.astral.sh/uv/)
- [ruff Documentation](https://docs.astral.sh/ruff/)

## License

MIT
