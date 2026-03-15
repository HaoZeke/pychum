# Contributing to pychum

Thank you for your interest in contributing to pychum! This document provides guidelines and instructions for contributing.

## Development Setup

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/HaoZeke/pychum
cd pychum

# Install in development mode
uv sync --all-extras

# Or with pip
pip install -e ".[dev,test,docs]"
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test categories
uv run pytest -m unit
uv run pytest -m integration

# Run with coverage
uv run pytest --cov=pychum --cov-report=html
```

## Code Style

We use the following tools for code quality:

- **pre-commit**: Git hooks for automated checks
- **ruff**: Fast Python linter and formatter
- **mypy**: Static type checking

### Setting up pre-commit

```bash
uv run pre-commit install
```

Pre-commit hooks will run automatically on `git commit`.

### Manual linting

```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Type checking
uv run mypy pychum/
```

## Adding New Engine Support

To add support for a new computational chemistry engine:

1. **Create the engine module** in `pychum/engine/<engine_name>/`

2. **Add Jinja2 templates** for input blocks in `_blocks/`

3. **Create dataclasses** for configuration in `dataclasses/`

4. **Update config_loader.py** to parse TOML configuration

5. **Add tests** in `tests/test_<engine_name>/`

### Example: Adding a New ORCA Block

1. Create the Jinja2 template:

```jinja2
# pychum/engine/orca/_blocks/new_block.jinja
%newblock
    {{ parameter1 }} {{ value1 }}
    {{ parameter2 }} {{ value2 }}
```

2. Add the dataclass:

```python
# pychum/engine/orca/dataclasses/new_block.py
from dataclasses import dataclass

@dataclass
class NewBlock:
    parameter1: str
    value1: float
    parameter2: str
    value2: int
```

3. Update config loader to recognize the new block

4. Add tests:

```python
# tests/test_orca/test_new_block.py
def test_new_block_generation():
    # Test input file generation
    pass
```

## Documentation

Documentation is written in orgmode and converted to reStructuredText for Sphinx.

### Building Documentation

```bash
cd docs
uv run sphinx-build source/ build/
```

### Adding Documentation

1. Add orgmode files in `docs/orgmode/`
2. Update `docs/orgmode/index.org` toctree
3. Build to verify: `uv run sphinx-build source/ build/`

## Pull Request Process

1. **Create an issue** for the feature or bug you're addressing
2. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** with tests
4. **Ensure all checks pass**:
   ```bash
   uv run pytest
   uv run ruff check .
   uv run mypy pychum/
   ```
5. **Update documentation** if needed
6. **Submit a pull request**

## Issue Tracking

We use [GitHub Issues](https://github.com/HaoZeke/pychum/issues) for tracking work.

### Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Documentation improvements
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed

## Code of Conduct

Please note that this project is released with a [Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## Questions?

- Open an issue for bugs or feature requests
- Use GitHub Discussions for general questions
- See existing documentation at https://pychum.rgoswami.me
