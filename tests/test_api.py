"""Tests for the simuci public API surface — __init__.py."""

from __future__ import annotations

import simuci


class TestPublicAPI:
    """Ensure the public API is intact and versioned."""

    def test_version_string(self) -> None:
        assert isinstance(simuci.__version__, str)
        parts = simuci.__version__.split(".")
        assert len(parts) == 3

    def test_all_exports_importable(self) -> None:
        for name in simuci.__all__:
            obj = getattr(simuci, name, None)
            assert obj is not None, f"{name} is in __all__ but not importable"

    def test_expected_exports(self) -> None:
        expected = {
            "Experiment",
            "Simulation",
            "single_run",
            "multiple_replication",
            "clustering",
            "clear_centroid_cache",
            "Wilcoxon",
            "Friedman",
            "SimulationMetrics",
            "StatsUtils",
            "validate_experiment_inputs",
            "validate_simulation_runs",
            "CentroidLoader",
        }
        assert expected == set(simuci.__all__)
