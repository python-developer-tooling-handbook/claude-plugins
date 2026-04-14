# Claude Code Plugins: Python Developer Tooling Handbook

Claude Code plugins from the [Python Developer Tooling Handbook](https://pydevtools.com). These plugins enforce modern Python tooling practices, automate common workflows, and provide guided migration paths for projects still using legacy tools.

## Installation

Add the marketplace:

```bash
/plugin marketplace add python-developer-tooling-handbook/claude-plugins
```

Then install the pydevtools plugin:

```bash
/plugin install pydevtools@python-tooling-handbook
```

## pydevtools

The primary plugin. It combines hooks that enforce best practices in real time with skills that handle multi-step Python tooling workflows.

### Skills

| Skill | What it does |
|---|---|
| `new-project` | Scaffold a Python project with uv, pytest, ruff, and pre-commit |
| `migrate-from-poetry` | Convert a Poetry project to uv (pyproject.toml rewrite, lock migration, CI updates) |
| `migrate-from-pip` | Convert requirements.txt projects to uv with a proper pyproject.toml |
| `migrate-from-mypy` | Migrate type checking configuration from mypy to ty |
| `audit` | Audit a project's tooling setup and recommend improvements |
| `publish` | Build and publish a package to PyPI using uv and trusted publishing |

### Hooks

| Hook | Event | What it does |
|---|---|---|
| `enforce-uv` | PreToolUse (Bash) | Intercepts pip/pip3/pipx/poetry commands and rewrites them to use uv |
| `ruff-after-edit` | PostToolUse (Write, Edit) | Runs ruff check and ruff format on Python files after every edit |
| `workflow-reminders` | UserPromptSubmit | Injects context-aware reminders about Python tooling best practices |
| `session-context` | SessionStart | Detects the project's Python tooling stack and loads relevant context |

## Deprecated: new-python-project

The original `new-python-project` plugin is still available but superseded by `pydevtools`, which includes the same project scaffolding capability (as the `new-project` skill) along with migration skills, enforcement hooks, and more.

To install the deprecated plugin:

```bash
/plugin install new-python-project@python-tooling-handbook
```

## Requirements

- [Claude Code](https://claude.com/claude-code)
- Python 3.9+
- [uv](https://docs.astral.sh/uv/) (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

## Learn More

- [Python Developer Tooling Handbook](https://pydevtools.com)
- [Claude Code Plugins Documentation](https://code.claude.com/docs/en/plugins)
- [Claude Code Marketplaces Documentation](https://code.claude.com/docs/en/plugin-marketplaces)
- [uv Documentation](https://docs.astral.sh/uv/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [ty Documentation](https://docs.astral.sh/ty/)

## License

MIT
