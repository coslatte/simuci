"""Type aliases for the simuci simulation engine."""

from __future__ import annotations

from typing import Any, Sequence, TypeAlias, Union

import numpy as np

# ---------------------------------------------------------------------------
# Core aliases
# ---------------------------------------------------------------------------

ClusterId: TypeAlias = int
"""Cluster index returned by :func:`simuci.distribuciones.clustering` (0, 1, or 2)."""

SimulationResult: TypeAlias = dict[str, int]
"""Single-replication result mapping variable labels to hour values."""

ArrayLike1D: TypeAlias = Union[Sequence[float], np.ndarray]
"""Anything that can act as a 1-D array of floats."""

Metric: TypeAlias = Union[tuple[float, ...], dict[str, Any]]
"""Return type of individual metric calculations in :class:`SimulationMetrics`."""
