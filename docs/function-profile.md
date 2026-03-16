# Function Profile

This document profiles each function and method in `simuci`, module by module.

## `src/simuci/core/experiment.py`

- `Experiment.__init__(...)`
  - Initializes patient-level input fields.
  - Optionally validates all input parameters through `validate_experiment_inputs`.
  - Prepares an empty mutable `result` dictionary.
- `Experiment.init_results_variables()`
  - Resets `result` keys using `EXPERIMENT_VARIABLES_LABELS` and sets values to `0`.
- `single_run(experiment, *, centroids_path)`
  - Resets result variables.
  - Classifies the experiment into a cluster using centroid-based nearest distance.
  - Runs one SimPy process (`Simulation.uci`) and returns the populated result dictionary.
- `multiple_replication(experiment, n_reps=100, as_int=True, *, centroids_path)`
  - Repeats `single_run` for `n_reps` replications.
  - Coerces values to numeric, normalizes invalid values to `0.0`, and returns a typed DataFrame.

## `src/simuci/core/simulation.py`

- `Simulation.__init__(experiment, cluster)`
  - Stores the active experiment and selected cluster id.
- `Simulation.uci(env)`
  - Selects cluster-specific distribution samplers.
  - Draws ICU-stage durations (`pre_vam`, `vam`, `post_vam`, `uci`, `post_uci`).
  - Enforces `vam <= uci` with capped retries and final clamp behavior.
  - Writes timeline results into `experiment.result`.
  - Advances simulated time through sequential `env.timeout(...)` yields.

## `src/simuci/core/distributions.py`

- `_sample_exponential(mean)`
  - Draws one scalar sample from an exponential distribution parameterized by `mean`.
- `_sample_weibull(shape, scale)`
  - Draws one scalar sample from a Weibull-minimum distribution.
- `tiemp_VAM_cluster0()`
  - Exponential sampler for cluster-0 VAM time.
- `tiemp_postUCI_cluster0()`
  - Mixture-model sampler for cluster-0 post-ICU time using three uniform branches.
- `estad_UTI_cluster0()`
  - Weibull sampler for cluster-0 ICU stay.
- `tiemp_VAM_cluster1()`
  - Exponential sampler for cluster-1 VAM time.
- `tiemp_postUCI_cluster1()`
  - Weibull sampler for cluster-1 post-ICU time.
- `estad_UTI_cluster1()`
  - Weibull sampler for cluster-1 ICU stay.
- `_load_centroids(path)`
  - Loads centroid data via `CentroidLoader` and caches arrays by file path.
- `clear_centroid_cache()`
  - Clears in-memory centroid cache so future calls reload files.
- `clustering(..., *, centroids_path)`
  - Builds the feature vector from patient parameters.
  - Adds derived `va_group` feature.
  - Computes Euclidean distance to centroids and returns nearest cluster index.

## `src/simuci/io/loaders/base.py`

- `BaseLoader.load(path)`
  - Abstract method contract for concrete loaders.
  - Requires loading and schema validation with explicit failure modes.

## `src/simuci/io/loaders/csv_loader.py`

- `CentroidLoader.load(path)`
  - Loads centroid CSV from disk.
  - Ensures minimum numeric feature columns are present.
  - Warns when row count differs from expected cluster count.
  - Returns a numeric array with the first `N_CLUSTERING_FEATURES` columns.

## `src/simuci/io/process_data.py`

- `load_file(path, column)`
  - Reads patient CSV with date parsing.
  - Applies type normalization (`tiempo_vam`, categorical diagnosis).
  - Sorts by admission date and returns a selected column list.
- `_iter_column(path, column)`
  - Internal generator over sorted values from a selected column.
- `get_fecha_ingreso(path)`
  - Yields `(next_date, current_date)` tuples across sorted admission dates.
- `get_fecha_egreso(path)`
  - Yields sorted discharge dates.
- `get_fecha_ing_uci(path)`
  - Yields sorted ICU admission dates.
- `get_tiempo_vam(path)`
  - Yields sorted VAM durations.
- `get_fecha_egr_uci(path)`
  - Yields sorted ICU discharge dates.
- `get_estadia_uci(path)`
  - Yields sorted ICU stay durations.
- `get_sala_egreso(path)`
  - Yields sorted discharge ward values.
- `get_evolucion(path)`
  - Yields sorted patient outcome values.
- `get_diagnostico(path)`
  - Yields sorted pre-ICU diagnosis values.
- `get_diagnostico_list(path)`
  - Returns unique diagnosis values from the source CSV.
- `get_time_simulation(path)`
  - Computes simulation horizon hours from earliest admission to latest discharge.

## `src/simuci/validation/validators.py`

- `_check_range(name, value, lo, hi)`
  - Internal guard for inclusive numeric ranges.
  - Raises `ValueError` with explicit limits when invalid.
- `_check_key(name, value, mapping)`
  - Internal guard for categorical values constrained by dictionary keys.
  - Raises `ValueError` with allowed key list when invalid.
- `validate_experiment_inputs(...)`
  - Validates all experiment fields against domain constraints.
  - Checks range-based and categorical parameters, including 4 diagnosis inputs.
- `validate_simulation_runs(n_reps)`
  - Validates replication count against configured min/max boundaries.

## `src/simuci/analysis/stats.py`

### `Wilcoxon`

- `Wilcoxon.test()`
  - Executes paired Wilcoxon signed-rank test.
  - Special-cases identical samples to `(statistic=0.0, p_value=1.0)`.

### `Friedman`

- `Friedman.test()`
  - Executes Friedman chi-square test for related samples.

### `SimulationMetrics`

- `SimulationMetrics.evaluate(confidence_level=0.95, random_state=None, result_as_dict=False)`
  - Runs full metric suite: coverage, error margins, KS test, AD test.
  - Stores computed results in object attributes.
- `SimulationMetrics._calculate_coverage_percentage(confidence_level=0.95)`
  - Computes percentage of true observations inside simulated confidence intervals.
- `SimulationMetrics._confidence_bounds(simulation_data, n_replicates, confidence_level)`
  - Computes lower/upper CI bounds per patient and variable using t-distribution.
- `SimulationMetrics._aligned_true_and_simulated()`
  - Aligns true data shape with simulation means for error metrics.
- `SimulationMetrics._calculate_rmse()`
  - Computes RMSE from aligned true and simulated means.
- `SimulationMetrics._calculate_mae()`
  - Computes MAE from aligned true and simulated means.
- `SimulationMetrics._calculate_mape()`
  - Computes MAPE with safe handling of zero-valued denominators.
- `SimulationMetrics._calculate_error_margin(as_dict=False)`
  - Returns `(rmse, mae, mape)` tuple or keyed dictionary.
- `SimulationMetrics._ks_single(sample_a, sample_b)`
  - Executes one two-sample KS test.
- `SimulationMetrics._ks_test_flat(as_dict)`
  - KS test path when simulation input is not 3-D.
- `SimulationMetrics._ks_test_per_variable(as_dict)`
  - Executes KS per variable for 3-D simulation data and aggregates result.
- `SimulationMetrics._ks_test(as_dict=False)`
  - Dispatcher to flat or per-variable KS branch.
- `SimulationMetrics._run_anderson_ksamp(real_sample, simulated_sample)`
  - Executes Anderson-Darling k-sample test with compatibility fallbacks.
- `SimulationMetrics._flatten_for_ad_test()`
  - Flattens true/sim data for AD testing; uses simulation means for 3-D inputs.
- `SimulationMetrics._ad_test(as_dict=False, *, rng=None)`
  - Runs Anderson-Darling comparison on sampled real vs simulated data.
- `SimulationMetrics._variable_label(index)`
  - Maps output variable index to human-readable label.
- `SimulationMetrics._align_shape(arr, target_shape)`
  - Performs best-effort shape alignment through reshape/resize.
- `SimulationMetrics._coerce_true_data(n_patients, n_variables)`
  - Coerces `true_data` into expected 2-D shape for coverage calculations.
- `SimulationMetrics._coerce_1d(td, n_patients, n_variables)`
  - Coercion path for 1-D `true_data` arrays.
- `SimulationMetrics._coerce_2d(td, n_patients, n_variables)`
  - Coercion path for 2-D `true_data` arrays.

### `StatsUtils`

- `StatsUtils.confidence_interval(mean, std, n, confidence=0.95)`
  - Computes confidence interval bounds from summary statistics.

## `src/simuci/tooling/envcheck.py`

- `run_environment_check(...)`
  - High-level environment diagnostics entry point.
  - Validates dependencies, importability, and optional vulnerability scanning.
- `_resolve_project_root(project_root)`
  - Resolves project root manually or via parent-directory walk.
- `_load_declared_requirements(project_root, *, include_extras)`
  - Reads dependency declarations from `pyproject.toml`.
- `_check_requirements(requirements)`
  - Compares declared requirements against installed packages and versions.
  - Includes local helper functions:
    - `parse_req(req)` (packaging path): requirement parser using `packaging`.
    - `is_satisfied(installed, spec)` (packaging path): version-spec evaluator.
    - `parse_req(req)` (fallback path): minimal parser when `packaging` is unavailable.
    - `is_satisfied(installed, spec)` (fallback path): permissive fallback evaluator.
- `_check_public_imports()`
  - Performs import smoke checks on public modules.
- `_run_pip_audit_best_effort()`
  - Best-effort vulnerability scan integration via `pip-audit` JSON output.
- `_format_report(report)`
  - Produces a human-readable report string from check results.
- `main(argv=None)`
  - CLI entry point for environment checks and optional audit flags.

## `src/simuci/envcheck.py`

- Module-level shim behavior
  - Exposes the tooling CLI through `python -m simuci.envcheck` by delegating to `simuci.tooling.envcheck.main`.
