"""Tests for simuci.schemas — PatientSchema."""

from __future__ import annotations

from simuci.schemas import PatientSchema


class TestPatientSchema:
    """Verify PatientSchema structure."""

    def test_date_columns(self) -> None:
        schema = PatientSchema()
        assert len(schema.date_columns) == 4
        assert "fecha_ingreso" in schema.date_columns

    def test_numeric_columns(self) -> None:
        schema = PatientSchema()
        assert "tiempo_vam" in schema.numeric_columns
        assert "estadia_uci" in schema.numeric_columns

    def test_categorical_columns(self) -> None:
        schema = PatientSchema()
        assert "diagnostico_preuci" in schema.categorical_columns

    def test_all_columns(self) -> None:
        schema = PatientSchema()
        all_cols = schema.all_columns
        assert len(all_cols) == 4 + 2 + 3  # date + numeric + categorical
        # No duplicates
        assert len(all_cols) == len(set(all_cols))
