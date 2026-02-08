"""Shared fixtures for simuci tests."""

from __future__ import annotations

import pytest

from simuci import Experiment

# ---------------------------------------------------------------------------
# Valid default kwargs — reuse across tests via `valid_params` fixture
# ---------------------------------------------------------------------------

VALID_EXPERIMENT_KWARGS: dict = {
    "age": 55,
    "diagnosis_admission1": 11,
    "diagnosis_admission2": 0,
    "diagnosis_admission3": 0,
    "diagnosis_admission4": 0,
    "apache": 20,
    "respiratory_insufficiency": 5,
    "artificial_ventilation": 1,
    "uti_stay": 100,
    "vam_time": 50,
    "preuti_stay_time": 10,
    "percent": 3,
}
"""A set of valid experiment parameters within all limits."""


@pytest.fixture()
def valid_params() -> dict:
    """Return a copy of valid experiment kwargs (safe to mutate)."""
    return VALID_EXPERIMENT_KWARGS.copy()


@pytest.fixture()
def experiment(valid_params: dict) -> Experiment:
    """Return a validated Experiment instance with default valid params."""
    return Experiment(**valid_params)
