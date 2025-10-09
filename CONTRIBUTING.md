### Contributing Guidelines

Thank you for considering contributing to QuantResearchStarter!

#### Getting Started
- Fork the repo and create your branch from `main`.
- Python 3.10+ is required.
- Install in editable mode: `pip install -e .[dev]`.
- Run tests and linters locally: `make test` and `make lint`.

#### Development Workflow
- Create a focused branch: `feature/<short-name>` or `fix/<short-name>`.
- Write unit tests for new features and bug fixes.
- Ensure `ruff` and `black` pass.
- Update documentation and docstrings as needed.

#### Pull Requests
- Fill in the PR template.
- Keep PRs small and focused.
- Include before/after behavior when applicable.
- Link related issues.

#### Good First Issues
- Look for issues labeled `good-first-issue` or `help-wanted`.
- Comment on an issue to get assigned.

#### Code Style
- Follow PEP8 with `ruff` and `black` formatting.
- Use type hints for public functions.
- Keep functions small and readable.

#### Testing
- Tests live under `tests/` and run with `pytest`.
- Aim for ~70% coverage of core modules.

#### Commit Messages
- Use imperative tone: "Add X", "Fix Y".
- Reference issues: `Fixes #123`.

#### Security
- See `SECURITY.md` to report vulnerabilities.

We appreciate your contributions!



