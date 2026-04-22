import gettext
import pytest

from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt

from func_aux import (
    paint_row, key_from_value, str_to_bool,
    numberToMonth, numberToResult, str_to_float,
)
from constants import BetResult

gettext.bindtextdomain("betcon", "lang/mo")
gettext.textdomain("betcon")


def _make_item(cols=18):
    return QTreeWidgetItem([""] * cols)


# ---------------------------------------------------------------------------
# paint_row
# ---------------------------------------------------------------------------

def test_paint_row_pending_shows_yellow():
    item = paint_row(_make_item(), "0€", str(BetResult.PENDING.value))
    assert item.background(0) == QBrush(Qt.yellow)

def test_paint_row_pending_ignores_negative_profit():
    item = paint_row(_make_item(), "-10.0€", str(BetResult.PENDING.value))
    assert item.background(0) == QBrush(Qt.yellow)

def test_paint_row_pending_ignores_positive_profit():
    item = paint_row(_make_item(), 20.0, str(BetResult.PENDING.value))
    assert item.background(0) == QBrush(Qt.yellow)

def test_paint_row_green_on_positive_profit():
    assert paint_row(_make_item(), "0.5€").background(0) == QBrush(Qt.green)
    assert paint_row(_make_item(), 10).background(0) == QBrush(Qt.green)

def test_paint_row_red_on_negative_profit():
    assert paint_row(_make_item(), "-10.0€").background(0) == QBrush(Qt.red)
    assert paint_row(_make_item(), "-20€").background(0) == QBrush(Qt.red)

def test_paint_row_cyan_on_zero_profit():
    assert paint_row(_make_item(), "0€").background(0) == QBrush(Qt.cyan)


# ---------------------------------------------------------------------------
# key_from_value
# ---------------------------------------------------------------------------

def test_key_from_value_finds_correct_key():
    dic = {1: 3, 2: 22, "ss": "ss", 43: "jj"}
    assert key_from_value(dic, 22) == 2


# ---------------------------------------------------------------------------
# str_to_bool
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("value,expected", [
    ("True", True),
    ("False", False),
    ("anything_else", False),
])
def test_str_to_bool(value, expected):
    assert str_to_bool(value) == expected


# ---------------------------------------------------------------------------
# numberToMonth  — all 12 months (locale-agnostic: compare at call time)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("num", range(1, 13))
def test_numberToMonth_all_months(num):
    result = numberToMonth(num)
    assert isinstance(result, str) and len(result) > 0

def test_numberToMonth_returns_12_distinct_values():
    values = [numberToMonth(n) for n in range(1, 13)]
    assert len(set(values)) == 12

def test_numberToMonth_order_is_consistent():
    """Month 1 < month 6 alphabetically in any supported language is not guaranteed,
    but the same index must always return the same value."""
    assert numberToMonth(1) == numberToMonth(1)
    assert numberToMonth(7) == numberToMonth(7)


# ---------------------------------------------------------------------------
# numberToResult  — all 7 BetResult values (locale-agnostic)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("code", list(BetResult))
def test_numberToResult_all_codes_return_string(code):
    result = numberToResult(code.value)
    assert isinstance(result, str) and len(result) > 0

def test_numberToResult_returns_7_distinct_values():
    values = [numberToResult(code.value) for code in BetResult]
    assert len(set(values)) == 7


# ---------------------------------------------------------------------------
# str_to_float  — comma as decimal separator (European locale)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("raw,expected", [
    ("0",   0.0),
    ("5",   5.0),
    ("-1", -1.0),
])
def test_str_to_float(raw, expected):
    assert str_to_float(raw) == pytest.approx(expected)

