"""simuci — ICU discrete-event simulation engine.

Public API
----------
Core simulation:
    Experiment, single_run, multiple_replication, Simulation

Clustering & distributions:
    clustering, clear_centroid_cache

Statistical validation:
    Wilcoxon, Friedman, SimulationMetrics, StatsUtils

Input validation:
    validate_experiment_inputs, validate_simulation_runs

Data loading:
    CentroidLoader

CSV utilities:
    procesar_datos  (sub-module)
"""

from __future__ import annotations

from simuci.distributions import clear_centroid_cache, clustering
from simuci.experiment import Experiment, multiple_replication, single_run
from simuci.loaders import CentroidLoader
from simuci.simulation import Simulation
from simuci.stats import Friedman, SimulationMetrics, StatsUtils, Wilcoxon
from simuci.validators import validate_experiment_inputs, validate_simulation_runs

__version__ = "0.1.0"

__all__ = [
    # Core
    "Experiment",
    "Simulation",
    "single_run",
    "multiple_replication",

    # Clustering
    "clustering",
    "clear_centroid_cache",

    # Statistics
    "Wilcoxon",
    "Friedman",
    "SimulationMetrics",
    "StatsUtils",

    # Validation
    "validate_experiment_inputs",
    "validate_simulation_runs",

    # Loaders
    "CentroidLoader",
]
