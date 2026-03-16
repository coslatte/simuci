"""Tests for simuci.io.process_data CSV extraction helpers."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from simuci.io.process_data import (
    get_diagnostico,
    get_diagnostico_list,
    get_estadia_uci,
    get_evolucion,
    get_fecha_egr_uci,
    get_fecha_egreso,
    get_fecha_ing_uci,
    get_fecha_ingreso,
    get_sala_egreso,
    get_tiempo_vam,
    get_time_simulation,
    load_file,
)


@pytest.fixture()
def patients_csv(tmp_path: Path) -> Path:
    """Create a minimal valid patient CSV for process_data helpers."""

    data = {
        "fecha_ingreso": ["2024-01-02", "2024-01-01", "2024-01-03"],
        "fecha_egreso": ["2024-01-10", "2024-01-05", "2024-01-11"],
        "fecha_ing_uci": ["2024-01-03", "2024-01-02", "2024-01-04"],
        "fecha_egr_uci": ["2024-01-08", "2024-01-04", "2024-01-09"],
        "tiempo_vam": [20, 10, 30],
        "diagnostico_preuci": [11, 11, 20],
        "estadia_uci": [120, 80, 140],
        "sala_egreso": ["A", "B", "A"],
        "evolucion": ["alive", "alive", "deceased"],
    }
    df = pd.DataFrame(data)

    csv_path = tmp_path / "patients.csv"
    df.to_csv(csv_path)

    return csv_path


def test_load_file_sorts_by_fecha_ingreso(patients_csv: Path) -> None:
    values = load_file(patients_csv, "tiempo_vam")

    # Sorted by fecha_ingreso: 2024-01-01, 2024-01-02, 2024-01-03
    assert values == [10, 20, 30]


def test_get_fecha_ingreso_returns_pairs(patients_csv: Path) -> None:
    pairs = list(get_fecha_ingreso(patients_csv))

    assert len(pairs) == 3
    assert pairs[0][0] >= pairs[0][1]


def test_column_generators_match_sorted_columns(patients_csv: Path) -> None:
    assert list(get_fecha_egreso(patients_csv)) == load_file(patients_csv, "fecha_egreso")
    assert list(get_fecha_ing_uci(patients_csv)) == load_file(patients_csv, "fecha_ing_uci")
    assert list(get_tiempo_vam(patients_csv)) == [10, 20, 30]
    assert list(get_fecha_egr_uci(patients_csv)) == load_file(patients_csv, "fecha_egr_uci")
    assert list(get_estadia_uci(patients_csv)) == [80, 120, 140]
    assert list(get_sala_egreso(patients_csv)) == ["B", "A", "A"]
    assert list(get_evolucion(patients_csv)) == ["alive", "alive", "deceased"]
    assert list(get_diagnostico(patients_csv)) == [11, 11, 20]


def test_get_diagnostico_list_unique_values(patients_csv: Path) -> None:
    values = get_diagnostico_list(patients_csv)

    assert set(values) == {11, 20}


def test_get_time_simulation_in_hours(patients_csv: Path) -> None:
    hours = get_time_simulation(patients_csv)

    # Earliest admission: 2024-01-01, latest discharge: 2024-01-11
    assert hours == 10 * 24
