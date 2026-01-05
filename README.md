# Claude Code Plugins: Python Developer Tooling Handbook

Claude Code plugins from the [Python Developer Tooling Handbook](https://pythontooling.com).

## Installation

Install all plugins from this collection:

```bash
/plugin install python-developer-tooling-handbook/claude-plugins
```

Or add globally:

```bash
/plugin install --global python-developer-tooling-handbook/claude-plugins
```

## Available Skills

### new-python-project

Set up Python projects with modern tooling:

- **uv** for package and environment management
- **pytest** for testing with coverage
- **ruff** for linting and formatting
- **pre-commit** for automated code quality
- **mypy** for type checking (optional)

**Usage examples:**
- "Set up a new Python project called my-tool"
- "Create a CLI package named mycli"
- "Add pytest and ruff to this project"
- "Convert this to a proper Python package"

## Plugin Structure

```
.claude-plugin/
└── plugin.json              # Plugin manifest
skills/
└── new-python-project/
    └── SKILL.md             # Python project setup skill
```

## Requirements

- [uv](https://docs.astral.sh/uv/) must be installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

## Learn More

- [Python Developer Tooling Handbook](https://pythontooling.com)
- [Claude Code Plugins Documentation](https://code.claude.com/docs/en/plugins)
- [uv Documentation](https://docs.astral.sh/uv/)
- [ruff Documentation](https://docs.astral.sh/ruff/)

## License

MIT
