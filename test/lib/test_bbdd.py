"""Tests for src/lib/bbdd.py using an isolated in-memory SQLite database.

The `db_memory` fixture (defined in test/conftest.py) monkeypatches Bbdd's
class-level directory/name attributes so every Bbdd() instantiated during
the test writes to a temporary file that is discarded afterwards.
"""
import pytest
from bbdd import Bbdd


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _insert_tipster(bd, name="TestTipster"):
    bd.insert(["name"], [name], "tipster")
    return bd.getId(name, "tipster")


def _insert_sport(bd, name="TestSport"):
    bd.insert(["name"], [name], "sport")
    return bd.getId(name, "sport")


def _insert_bet(bd, *, date="2024-01-15 12:00", sport_id=1, competition_id=1,
                region_id=1, bookie_id=1, market_id=1, tipster_id=1,
                stake=5, one=100, result=0, profit=0.0, bet=50.0, quota=2.0):
    columns = ["date", "sport", "competition", "region", "player1", "player2",
               "pick", "bookie", "market", "tipster", "stake", "one",
               "result", "profit", "bet", "quota", "free"]
    values = [date, sport_id, competition_id, region_id, "Team A", "Team B",
              "1", bookie_id, market_id, tipster_id, stake, one,
              result, profit, bet, quota, 0]
    bd.insert(columns, values, "bet")
    return bd.max("bet", "id")


# ---------------------------------------------------------------------------
# insert / select
# ---------------------------------------------------------------------------

def test_insert_and_select(db_memory):
    db_memory.insert(["name"], ["NewTipster"], "tipster")
    rows = db_memory.select("tipster", where="name='NewTipster'")
    assert len(rows) == 1
    assert rows[0][1] == "NewTipster"


def test_insert_returns_zero_on_success(db_memory):
    rc = db_memory.insert(["name"], ["AnotherTipster"], "tipster")
    assert rc == 0


def test_insert_returns_minus_one_on_error(db_memory):
    # Bookie has a UNIQUE index on name — duplicate triggers an error
    db_memory.insert(["name"], ["DupBookie"], "bookie")
    rc = db_memory.insert(["name"], ["DupBookie"], "bookie")
    assert rc == -1


# ---------------------------------------------------------------------------
# update
# ---------------------------------------------------------------------------

def test_update_changes_value(db_memory):
    tipster_id = _insert_tipster(db_memory, "OldName")
    db_memory.update(["name"], ["NewName"], "tipster", f"id={tipster_id}")
    rows = db_memory.select("tipster", where=f"id={tipster_id}")
    assert rows[0][1] == "NewName"


def test_update_with_special_chars(db_memory):
    """Values containing quotes must not cause SQL errors after parametrization."""
    tipster_id = _insert_tipster(db_memory, "Normal")
    rc = db_memory.update(["name"], ["O'Brien"], "tipster", f"id={tipster_id}")
    assert rc == 0
    rows = db_memory.select("tipster", where=f"id={tipster_id}")
    assert rows[0][1] == "O'Brien"


# ---------------------------------------------------------------------------
# delete / deleteWhere
# ---------------------------------------------------------------------------

def test_delete_removes_row(db_memory):
    tipster_id = _insert_tipster(db_memory, "ToDelete")
    db_memory.delete("tipster", tipster_id)
    rows = db_memory.select("tipster", where=f"id={tipster_id}")
    assert rows == []


def test_deleteWhere_removes_matching_rows(db_memory):
    _insert_tipster(db_memory, "Gone1")
    _insert_tipster(db_memory, "Gone2")
    _insert_tipster(db_memory, "Keep")
    db_memory.deleteWhere("tipster", "name LIKE 'Gone%'")
    remaining = db_memory.select("tipster", where="name LIKE 'Gone%'")
    assert remaining == []
    kept = db_memory.select("tipster", where="name='Keep'")
    assert len(kept) == 1


# ---------------------------------------------------------------------------
# getValue / getId
# ---------------------------------------------------------------------------

def test_getValue_returns_name_by_id(db_memory):
    tipster_id = _insert_tipster(db_memory, "Lookup")
    assert db_memory.getValue(tipster_id, "tipster") == "Lookup"


def test_getId_returns_id_by_name(db_memory):
    _insert_tipster(db_memory, "Findme")
    tid = db_memory.getId("Findme", "tipster")
    assert tid is not None
    assert db_memory.getValue(tid, "tipster") == "Findme"


def test_getId_returns_none_for_missing(db_memory):
    assert db_memory.getId("DoesNotExist", "tipster") is None


def test_getId_safe_against_sql_injection(db_memory):
    """A value containing SQL metacharacters must be treated as a literal string."""
    result = db_memory.getId("' OR '1'='1", "tipster")
    assert result is None


# ---------------------------------------------------------------------------
# count / sum / max
# ---------------------------------------------------------------------------

def test_count_returns_correct_number(db_memory):
    initial = db_memory.count("tipster")
    _insert_tipster(db_memory, "C1")
    _insert_tipster(db_memory, "C2")
    assert db_memory.count("tipster") == initial + 2


def test_sum_aggregates_correctly(db_memory):
    _insert_bet(db_memory, profit=10.0)
    _insert_bet(db_memory, profit=5.0)
    total = db_memory.sum("bet", "profit")
    assert total == pytest.approx(15.0)


def test_max_returns_highest_value(db_memory):
    _insert_bet(db_memory, quota=3.5)
    _insert_bet(db_memory, quota=1.2)
    assert db_memory.max("bet", "quota") == pytest.approx(3.5)


# ---------------------------------------------------------------------------
# getDaysOfMonth (static)
# ---------------------------------------------------------------------------

def test_getDaysOfMonth_returns_days_present(db_memory):
    _insert_bet(db_memory, date="2024-03-01 10:00")
    _insert_bet(db_memory, date="2024-03-15 10:00")
    _insert_bet(db_memory, date="2024-04-01 10:00")  # Different month
    days = Bbdd.getDaysOfMonth("bet", "2024", "03")
    assert "01" in days
    assert "15" in days
    assert len(days) == 2


# ---------------------------------------------------------------------------
# isExist — tested implicitly by the db_memory fixture itself;
# a second Bbdd() in the same tmp_path should find the file.
# ---------------------------------------------------------------------------

def test_isExist_true_after_creation(db_memory):
    bd2 = Bbdd()
    assert bd2.isExist() is True
    bd2.close()
