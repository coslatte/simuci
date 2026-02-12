# GitHub Copilot Instructions for `simuci`

You are an expert Python developer specializing in Discrete-Event Simulation (DES), Statistics, and Healthcare Modeling.

## Project Context

- **Name**: `simuci` (ICU Discrete-Event Simulation Engine).
- **Domain**: Healthcare resource optimization, ICU capacity planning.
- **Core Stack**: Python 3.12+, SimPy, NumPy, Pandas, SciPy, Scikit-learn.
- **Tooling**: `uv` (dependency management), `pytest` (testing), `ruff` (linting/formatting), `mypy` (static typing).

## Code Style & Standards

- **Strict Typing**: All code MUST be fully typed. Use `typing` module or modern union syntax (`|`). No `Any` unless absolutely necessary.
- **Formatting**: Adhere to `ruff` defaults. Line length 88. Double quotes.
- **Docstrings**: Google-style docstrings.
- **SimPy Idioms**:
  - Always use correct generator syntax (`yield req`, `yield env.timeout()`).
  - Manage resources using `with resource.request() as req:` contexts.
  - Separate process logic (generators) from state management.

## Architecture & Modularity

- **`src/simuci/core/`**: Core simulation logic (Event, Process, Resources). Pure logic, minimal dependencies.
- **`src/simuci/io/`**: Data ingestion and export. Validation schemas live here or in `validation/`.
- **`src/simuci/analysis/`**: Statistical post-processing (NumPy/Pandas heavy). Contains `stats.py`.
- **`src/simuci/tooling/`**: Developer tools (`envcheck.py`).
- **`src/simuci/internals/`**: Private types and constants.

## Workflow & Commands

- **Dependency Management**: Prefer `uv` commands.
  - Run scripts: `uv run script.py`
  - Add deps: `uv add <package>`
  - Sync: `uv sync`
- **Environment Integrity**:
  - Run `python -m simuci.tooling.envcheck` to verify dependencies and imports.
  - Use `python -m simuci.tooling.envcheck --audit` for security checks.
- **Testing**:
  - Use `pytest`.
  - Place fixtures in `tests/conftest.py`.
  - Mock I/O heavy operations.
  - Validate statistical outcomes using `scipy.stats` (e.g., Chi-Square, K-S tests).

## Documentation

- The project is **Bilingual (English/Spanish)**.
- If you modify code that has documentation overrides (e.g., `README.md` and `README.es.md`), **update BOTH**.
- Keep technical terms consistent (e.g., "Length of Stay" / "Estancia", "Arrival Rate" / "Tasa de Llegada").
