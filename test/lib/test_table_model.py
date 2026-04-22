import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src", "lib"))

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from table_model import (
    BetconTableModel,
    paint_row_items,
    make_item,
    make_icon_item,
)
from constants import BetResult


@pytest.fixture(scope="module")
def qapp():
    return QApplication.instance() or QApplication([])


# ── BetconTableModel ────────────────────────────────────────────────────

def test_model_setup_sets_headers(qapp):
    model = BetconTableModel()
    model.setup(["#", "id", "Date", "Sport", "Profit"], hidden_col=1)
    assert model.columnCount() == 5
    assert model.horizontalHeaderItem(2).text() == "Date"


def test_model_get_id_returns_correct_value(qapp):
    model = BetconTableModel()
    model.setup(["#", "id", "Name"], hidden_col=1)
    row = [make_item("1"), make_item("42"), make_item("Fútbol")]
    model.appendRow(row)
    assert model.get_id(0) == "42"


def test_model_get_id_empty_model_returns_empty(qapp):
    model = BetconTableModel()
    model.setup(["#", "id"], hidden_col=1)
    assert model.get_id(0) == ""


# ── paint_row_items ──────────────────────────────────────────────────────

SKIP_ROLE = Qt.ItemDataRole.UserRole + 10


def _make_row(n=5):
    return [make_item(str(i)) for i in range(n)]


def test_paint_pending_sets_amber_background(qapp):
    items = _make_row()
    paint_row_items(items, profit=0.0, result=BetResult.PENDING)
    bg = items[0].background().color()
    assert bg == QColor("#5a4d00")


def test_paint_won_sets_green_background(qapp):
    items = _make_row()
    paint_row_items(items, profit=5.0, result=BetResult.WON)
    bg = items[0].background().color()
    assert bg == QColor("#1a4d2e")


def test_paint_lost_sets_red_background(qapp):
    items = _make_row()
    paint_row_items(items, profit=-3.0, result=BetResult.LOST)
    bg = items[0].background().color()
    assert bg == QColor("#4d1a1a")


def test_paint_draw_sets_cyan_background(qapp):
    items = _make_row()
    paint_row_items(items, profit=0.0, result=BetResult.VOID)
    bg = items[0].background().color()
    assert bg == QColor("#0d3040")


def test_paint_skips_items_with_skip_role(qapp):
    items = _make_row(3)
    items[1].setData(True, SKIP_ROLE)  # mark as skip
    paint_row_items(items, profit=5.0, result=BetResult.WON)
    # item[0] and item[2] should be green, item[1] should be untouched (no background set)
    assert items[0].background().color() == QColor("#1a4d2e")
    assert items[2].background().color() == QColor("#1a4d2e")
    assert items[1].background().color() != QColor("#1a4d2e")


def test_paint_stores_light_variant(qapp):
    items = _make_row(2)
    paint_row_items(items, profit=5.0, result=BetResult.WON)
    light_bg = items[0].data(Qt.ItemDataRole.UserRole + 11)
    assert light_bg == QColor("#c3e6cb")


# ── make_icon_item ───────────────────────────────────────────────────────

def test_make_icon_item_text_is_set(qapp):
    item = make_icon_item(None, "Fútbol")
    assert item.text() == "Fútbol"


def test_make_icon_item_is_not_editable(qapp):
    item = make_icon_item(None, "test")
    assert not item.isEditable()


def test_make_icon_item_skip_role_is_true(qapp):
    item = make_icon_item(None, "test")
    assert item.data(SKIP_ROLE) is True


def test_make_icon_item_bg_is_applied(qapp):
    bg = QColor("#ff0000")
    item = make_icon_item(None, "test", bg=bg)
    assert item.background().color() == bg


def test_make_icon_item_invalid_path_has_no_icon(qapp):
    item = make_icon_item("/nonexistent/path.png", "test")
    assert item.icon().isNull()


# ── make_item ────────────────────────────────────────────────────────────

def test_make_item_is_not_editable(qapp):
    item = make_item("hello")
    assert not item.isEditable()


def test_make_item_text(qapp):
    item = make_item("world")
    assert item.text() == "world"
