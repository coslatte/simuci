"""Data schemas and structured types for CSV inputs.

These schemas document the expected column structure so that loaders
can validate data without exposing proprietary datasets.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypedDict

# ---------------------------------------------------------------------------
# Centroid CSV schema
# ---------------------------------------------------------------------------


class CentroidRow(TypedDict):
    """Schema for a single centroid row (3 clusters × 18 numeric columns)."""

    cluster_id: int
    features: list[float]


@dataclass(frozen=True)
class CentroidSchema:
    """Describes the expected shape of the centroids CSV.

    The CSV has an index column (cluster id) and 18 numeric columns
    named ``"0"`` through ``"17"``.  Only the first
    :data:`~simuci._constants.N_CLUSTERING_FEATURES` columns are used
    by the clustering function.
    """

    n_clusters: int = 3
    n_total_columns: int = 18
    n_used_columns: int = 12
    index_column: str = ""
    feature_columns: list[str] = field(default_factory=lambda: [str(i) for i in range(18)])


# ---------------------------------------------------------------------------
# Patient CSV schema
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PatientSchema:
    """Describes the expected columns in a patient data CSV.

    Used by :mod:`simuci.procesar_datos` loaders.
    """

    date_columns: list[str] = field(
        default_factory=lambda: [
            "fecha_ingreso",
            "fecha_egreso",
            "fecha_ing_uci",
            "fecha_egr_uci",
        ]
    )
    numeric_columns: list[str] = field(
        default_factory=lambda: [
            "tiempo_vam",
            "estadia_uci",
        ]
    )
    categorical_columns: list[str] = field(
        default_factory=lambda: [
            "diagnostico_preuci",
            "sala_egreso",
            "evolucion",
        ]
    )

    @property
    def all_columns(self) -> list[str]:
        """Return every expected column name."""

        return self.date_columns + self.numeric_columns + self.categorical_columns
