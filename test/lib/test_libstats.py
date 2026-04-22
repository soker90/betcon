"""Tests for src/lib/libstats.py.

LibStats creates its own Bbdd() instances internally.  Since conftest.py
monkeypatches the same `bbdd.Bbdd` class (bare import, matching what
libstats.py uses), the db_memory fixture correctly redirects all database
access to the isolated temporary file.
"""
import pytest

from bbdd import Bbdd
from constants import BetResult
from libstats import LibStats

# Override coin symbol to avoid depending on ~/.betcon/config.yml in tests.
LibStats.coin = "€"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _seed_db(bd):
    """Insert minimal reference data and a handful of bets."""
    # Tipster
    bd.insert(["name"], ["Alice"], "tipster")
    bd.insert(["name"], ["Bob"], "tipster")
    alice_id = bd.getId("Alice", "tipster")
    bob_id   = bd.getId("Bob",   "tipster")

    # Sport
    bd.insert(["name"], ["Football"], "sport")
    sport_id = bd.getId("Football", "sport")

    # Bookie (already seeded from database.sql; grab id=1)
    bookie_id = 1

    # Market (already seeded)
    market_id = 1

    # Region / competition already seeded (id=1)
    region_id      = 1
    competition_id = 1

    cols = ["date", "sport", "competition", "region", "player1", "player2",
            "pick", "bookie", "market", "tipster", "stake", "one",
            "result", "profit", "bet", "quota", "free"]

    def _bet(date, tipster, result, profit, quota=2.0):
        bd.insert(cols, [date, sport_id, competition_id, region_id,
                         "A", "B", "1", bookie_id, market_id, tipster,
                         5, 100, result, profit, 50.0, quota, 0], "bet")

    # Alice: 2 won, 1 lost — all in 2024-01
    _bet("2024-01-10 10:00", alice_id, BetResult.WON.value,  10.0)
    _bet("2024-01-11 10:00", alice_id, BetResult.WON.value,   5.0)
    _bet("2024-01-12 10:00", alice_id, BetResult.LOST.value, -5.0)

    # Bob: 1 won in 2024-01, 1 pending in 2024-02
    _bet("2024-01-20 10:00", bob_id, BetResult.WON.value,    8.0)
    _bet("2024-02-05 10:00", bob_id, BetResult.PENDING.value, 0.0)

    return alice_id, bob_id, sport_id, bookie_id


@pytest.fixture
def seeded_db(db_memory):
    alice_id, bob_id, sport_id, bookie_id = _seed_db(db_memory)
    return db_memory, alice_id, bob_id, sport_id, bookie_id


# ---------------------------------------------------------------------------
# getTipster
# ---------------------------------------------------------------------------

def test_getTipster_no_filter_returns_rows(seeded_db):
    LibStats.coin = "€"
    rows = LibStats.getTipster()
    assert len(rows) > 0
    names = [r[0] for r in rows]
    assert "Alice" in names


def test_getTipster_with_date_filter(seeded_db):
    LibStats.coin = "€"
    rows = LibStats.getTipster(year="2024", month="01")
    assert len(rows) > 0
    names = [r[0] for r in rows]
    assert "Bob" in names  # Bob has a bet in 2024-01


def test_getTipster_excludes_pending_from_profit(seeded_db):
    """Pending bets (result=0) must not be counted in profit."""
    LibStats.coin = "€"
    rows = LibStats.getTipster(year="2024", month="02")
    # Bob's only bet in 2024-02 is pending, so profit row should be absent
    assert rows == []


# ---------------------------------------------------------------------------
# getBookie
# ---------------------------------------------------------------------------

def test_getBookie_no_filter(seeded_db):
    LibStats.coin = "€"
    rows = LibStats.getBookie()
    assert len(rows) > 0


def test_getBookie_with_date_filter(seeded_db):
    LibStats.coin = "€"
    rows = LibStats.getBookie(year="2024", month="01")
    assert len(rows) > 0


# ---------------------------------------------------------------------------
# getSport
# ---------------------------------------------------------------------------

def test_getSport_no_filter(seeded_db):
    LibStats.coin = "€"
    rows = LibStats.getSport()
    assert len(rows) > 0
    assert rows[0][0] == "Football"


def test_getSport_with_date_filter(seeded_db):
    LibStats.coin = "€"
    rows = LibStats.getSport(year="2024", month="01")
    assert len(rows) > 0


# ---------------------------------------------------------------------------
# getRegion
# ---------------------------------------------------------------------------

def test_getRegion_no_filter(seeded_db):
    LibStats.coin = "€"
    rows = LibStats.getRegion()
    assert len(rows) > 0


# ---------------------------------------------------------------------------
# getStake
# ---------------------------------------------------------------------------

def test_getStake_no_filter(seeded_db):
    LibStats.coin = "€"
    rows = LibStats.getStake()
    assert len(rows) > 0
    stakes = [float(r[0]) for r in rows]
    assert 5.0 in stakes


# ---------------------------------------------------------------------------
# getYears / getDaysOfMonth
# ---------------------------------------------------------------------------

def test_getYears_includes_seeded_year(seeded_db):
    years, _ = LibStats.getYears()
    assert "2024" in years


def test_getDaysOfMonth_returns_seeded_days(seeded_db):
    days = LibStats.getDaysOfMonth("2024", "01")
    assert "10" in days
    assert "11" in days
    assert "12" in days
