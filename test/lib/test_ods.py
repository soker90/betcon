"""Tests for src/lib/ods.py (export / import round-trip to CSV).

Uses pytest's tmp_path fixture for temporary files and db_memory (conftest.py)
to redirect all Bbdd instances to an isolated database.
"""
import pytest

from bbdd import Bbdd
from ods import Ods
from constants import BetResult


def _seed_bet(bd):
    cols = ["date", "sport", "competition", "region", "player1", "player2",
            "pick", "bookie", "market", "tipster", "stake", "one",
            "result", "profit", "bet", "quota", "free"]
    values = ["2024-06-01 10:00", 7, 7, 1, "Real Madrid", "Barcelona",
              "1", 1, 1, 1, 5, 100, BetResult.WON.value, 10.0, 50.0, 2.0, 0]
    bd.insert(cols, values, "bet")


# ---------------------------------------------------------------------------
# export
# ---------------------------------------------------------------------------

def test_export_creates_file(db_memory, tmp_path):
    _seed_bet(db_memory)
    csv_path = str(tmp_path / "export.csv")
    Ods(csv_path).export()

    import os
    assert os.path.exists(csv_path)


def test_export_file_is_nonempty(db_memory, tmp_path):
    _seed_bet(db_memory)
    csv_path = str(tmp_path / "export.csv")
    Ods(csv_path).export()

    import os
    assert os.path.getsize(csv_path) > 0


def test_export_with_empty_db_creates_file(db_memory, tmp_path):
    csv_path = str(tmp_path / "empty_export.csv")
    Ods(csv_path).export()

    import os
    assert os.path.exists(csv_path)


# ---------------------------------------------------------------------------
# import round-trip
# ---------------------------------------------------------------------------

def test_import_round_trip(db_memory, tmp_path):
    """Export a bet, then import it back into a fresh DB and verify it appears."""
    _seed_bet(db_memory)
    csv_path = str(tmp_path / "roundtrip.csv")

    # Export
    Ods(csv_path).export()

    # Clear bets
    db_memory.deleteWhere("bet", "1=1")
    assert db_memory.count("bet") == 0

    # Import
    result = Ods(csv_path).imports()
    assert result is None  # None = success (no error string returned)
    assert db_memory.count("bet") == 1

