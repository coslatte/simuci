# Plan: Clean `simuci` pip-installable module

**TL;DR**: Extract the simulation engine from `SimUci/uci/` into `simuci-module/` as a standalone pip-installable package using a `src/` layout. Only simulation logic ships — no real data, no Streamlit code, no model files. Three coupling points to `utils.constants` are resolved by inlining constants. A synthetic `df_centroides.csv` replaces the real one. Input validation is added (currently zero exists). The existing `SimUci/` app switches to `from simuci import ...` once the module is installed.

## Steps

### 1. Create `pyproject.toml`

In `simuci-module/` using modern PEP 621 metadata:

- `name = "simuci"`, `version = "0.1.0"`, `requires-python = ">=3.13"`
- Dependencies: `numpy`, `pandas`, `scipy`, `simpy`, `scikit-learn` (for `stats.py`)
- Build backend: `hatchling` with `src/` layout
- No `streamlit`, `matplotlib`, `plotly`, `joblib`, or `imbalanced-learn`
- Add optional `[project.optional-dependencies]` for `dev` (pytest, mypy, ruff)

### 2. Create the `src/simuci/` package tree

```
simuci-module/
├── pyproject.toml
├── README.md
├── LICENSE
└── src/
    └── simuci/
        ├── __init__.py
        ├── _constants.py
        ├── _types.py
        ├── distribuciones.py
        ├── experiment.py
        ├── simulacion.py
        ├── procesar_datos.py
        ├── stats.py
        ├── validators.py
        ├── schemas.py
        ├── loaders/
        │   ├── __init__.py
        │   ├── base.py
        │   └── csv_loader.py
        └── examples/
            └── sample_centroids.csv (examples package data, not real centroids) -> also adding documentation in README about how to use real centroids with the loader
```

### 3. Resolve coupling — `_constants.py` (internal module)

- Inline `EXPERIMENT_VARIABLES_LABELS` (5 strings from `utils/constants/experiment.py`) — used by `experiment.py` and `stats.py`
- Inline `EXPERIMENT_VARIABLES_FROM_CSV` (11 column names) — used only for `len()` in `distribuciones.py`, replace with `_N_FEATURES = 12` (the actual dimensionality used by `clustering()`)
- Move validation limits from `limits.py` (min/max/default for age, APACHE, etc.)
- Move category mappings from `mappings.py` (`VENTILATION_TYPE`, `PREUCI_DIAG`, `RESP_INSUF`)

### 4. Resolve coupling — `distribuciones.py`

- Remove `from utils.constants import DFCENTROIDES_CSV_PATH, EXPERIMENT_VARIABLES_FROM_CSV`
- Refactor `_load_centroids(path=None)` to accept an optional path; default uses `importlib.resources` to find `examples/sample_centroids.csv`
- Replace `_N_FEATURES = len(EXPERIMENT_VARIABLES_FROM_CSV)` with `_N_FEATURES = 12` (from `_constants`)

### 5. Resolve coupling — `experiment.py`

- Replace `from utils.constants import EXPERIMENT_VARIABLES_LABELS` with `from simuci._constants import EXPERIMENT_VARIABLES_LABELS`
- Change `from uci import distribuciones` → `from simuci import distribuciones`
- Change `from uci.simulacion import Simulation` → `from simuci.simulacion import Simulation`

### 6. Resolve coupling — `simulacion.py`

- Change `from uci import distribuciones` → `from simuci import distribuciones`
- Change TYPE_CHECKING import of `Experiment` to `from simuci.experiment import Experiment`

### 7. Resolve coupling — `stats.py`

- Replace `from utils.constants import EXPERIMENT_VARIABLES_LABELS` with `from simuci._constants import EXPERIMENT_VARIABLES_LABELS`

### 8. Copy `procesar_datos.py` as-is

No coupling to resolve.

### 9. Create `validators.py`

- Add `validate_experiment_inputs(age, apache, vam_time, uti_stay, preuti_stay, ...)` using the limits from `_constants` — currently NO validation exists in the engine, inputs pass unchecked to numpy
- Wire into `Experiment.__init__()` so invalid inputs raise `ValueError` with descriptive messages
- Validate `clustering()` inputs similarly

### 10. Create `schemas.py`

- Define expected column schemas for CSV inputs (centroids, patient data)
- Use dataclasses or TypedDicts for structured types

### 11. Create `_types.py`

- Type aliases for the module (e.g., `ClusterId`, `SimulationResult`)

### 12. Create `loaders/`

- `base.py`: abstract loader interface
- `csv_loader.py`: `load_centroids(path) -> pd.DataFrame` with schema validation, extracted from `distribuciones._load_centroids()`

### 13. Create `examples/sample_centroids.csv`

- Synthetic 3×18 CSV with randomized but structurally valid centroid data (same column count and sensible ranges, but NOT the real trained centroids)
- Register in `pyproject.toml` as package data

### 14. Create `__init__.py` — public API surface

- Export: `Experiment`, `single_run`, `multiple_replication`, `Simulation`, `clustering`, `Wilcoxon`, `Friedman`, `SimulationMetrics`, `StatsUtils`
- Export: `validate_experiment_inputs`
- Set `__version__ = "0.1.0"`
- Set `__all__`

### 15. Update `SimUci/` app to depend on the extracted module

- Add `simuci` to `requirements.txt`
- Replace `from uci.experiment import ...` → `from simuci import ...`
- Replace `from uci.stats import ...` → `from simuci import ...`
- Keep `utils/constants/paths.py`, `messages.py`, `theme.py`, `helpers/`, `validation_ui/`, `visuals/` in the app (Streamlit-specific)
- The real `df_centroides.csv` stays in `SimUci/data/` and is passed explicitly to `clustering()` or configured via the loader

## Verification

- `cd simuci-module && pip install -e .` succeeds with no errors
- `python -c "from simuci import Experiment, single_run, multiple_replication; print('OK')"` works
- `python -c "from simuci import clustering; print(clustering(55, 11, 0, 0, 0, 20, 5, 1, 500, 200, 10))"` returns a cluster ID (0 or 1)
- `python -c "from simuci.validators import validate_experiment_inputs; validate_experiment_inputs(age=200)"` raises `ValueError`
- `pytest` with basic unit tests for `single_run`, `clustering`, `SimulationMetrics`
- The `SimUci/` Streamlit app still runs correctly after switching imports to `simuci`

## Design Decisions

| Decision | Chosen | Rationale |
|----------|--------|-----------|
| Package layout | `src/` layout | Prevents accidental imports from source tree during development |
| Constants strategy | Inline into `_constants.py` | Only 3 small lists, not worth a shared package |
| Centroid data | Synthetic sample | User explicitly wants no real/proprietary data shipped |
| Build backend | `hatchling` | Simpler config for pure-Python packages, modern standard |
| Constants visibility | `_constants.py` (underscore-prefixed) | Keeps the module flat since only ~30 lines of constants |
| Input validation | In the module | Currently zero validation exists, fragile |
| `procesar_datos.py` | Included | Clean, no coupling, generic CSV utility logic |

## Issues Found (Blockers & Risks)

### Blocker: 3 coupling points to `utils.constants`

| File | Import | Resolution |
|------|--------|------------|
| `distribuciones.py` | `DFCENTROIDES_CSV_PATH` | Accept path param, default via `importlib.resources` |
| `distribuciones.py` | `EXPERIMENT_VARIABLES_FROM_CSV` | Replace with literal `_N_FEATURES = 12` |
| `experiment.py` | `EXPERIMENT_VARIABLES_LABELS` | Inline into `_constants.py` |
| `stats.py` | `EXPERIMENT_VARIABLES_LABELS` | Inline into `_constants.py` |

### Blocker: Hardcoded path in `distribuciones._load_centroids()`

`_load_centroids()` reads from `DFCENTROIDES_CSV_PATH` (resolved via `Path(__file__).parent.parent.parent / "data" / "df_centroides.csv"`). Must be refactored to accept a path parameter with a fallback to bundled sample data.

### Blocker: No input validation anywhere in the engine

`Experiment.__init__()` accepts raw values with no bounds checking. Invalid inputs (age=9999, negative APACHE, etc.) silently produce garbage results. The module must add validation.

### Risk: Hardcoded Spanish string keys in `simulacion.py`

`Simulation.uci()` writes results using hardcoded keys like `"Tiempo Pre VAM"`, `"Tiempo Post VAM"`, etc. These must match `EXPERIMENT_VARIABLES_LABELS` exactly. Fragile — should be centralized in `_constants.py`.

### Risk: `_N_FEATURES` mismatch

`_N_FEATURES = len(EXPERIMENT_VARIABLES_FROM_CSV)` evaluates to 11, but `clustering()` builds a 12-element feature vector (appends derived `va_group`). The constant and actual usage are misaligned.

### Risk: PyPI name `simuci` availability

Not verified. If taken, a fallback name like `simuci-sim` or a scoped name would be needed.

### Risk: `lru_cache` on `_load_centroids()` is global mutable state

Once centroids are loaded, changing the path has no effect unless the cache is cleared. The refactored version should handle this (e.g., cache per path, or drop caching in favor of explicit init).
