# Claude Code Plugin: New Python Project

A [Claude Code](https://claude.com/claude-code) plugin for setting up Python projects with modern tooling.

Part of the [Python Developer Tooling Handbook](https://pythontooling.com).

## What This Plugin Does

This plugin provides a skill that helps Claude Code set up Python projects using best practices:

- **uv** for package and environment management
- **pytest** for testing with coverage
- **ruff** for linting and formatting
- **pre-commit** for automated code quality
- **mypy** for type checking (optional)

It handles new projects, adding tooling to existing code, and converting legacy projects.

## Installation

Install the plugin using the Claude Code CLI:

```bash
/plugin install python-developer-tooling-handbook/claude-skill-new-python-project
```

Or add it globally:

```bash
/plugin install --global python-developer-tooling-handbook/claude-skill-new-python-project
```

## Usage

Once installed, ask Claude Code things like:

- "Set up a new Python project called my-tool"
- "Create a CLI package named mycli"
- "Add pytest and ruff to this project"
- "Convert this to a proper Python package"
- "Set up pre-commit hooks"

The skill will guide Claude to ask clarifying questions and apply the appropriate tooling.

## Plugin Structure

```
.claude-plugin/
└── plugin.json          # Plugin manifest
skills/
└── new-python-project/
    └── SKILL.md         # Skill definition
```

## Requirements

- [uv](https://docs.astral.sh/uv/) must be installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

## Learn More

- [Python Developer Tooling Handbook](https://pythontooling.com) - Comprehensive guide to modern Python tooling
- [Claude Code Plugins Documentation](https://code.claude.com/docs/en/plugins)
- [uv Documentation](https://docs.astral.sh/uv/)
- [ruff Documentation](https://docs.astral.sh/ruff/)

## License

MIT
