from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor, QIcon, QPixmap
from PySide6.QtCore import Qt
from constants import BetResult

# Result color palette — works on both dark and light themes
_RESULT_COLORS = {
    BetResult.PENDING: QColor("#6b5e00"),   # amber dark (readable on dark bg)
    "pending_light":   QColor("#fff3cd"),   # amber light (readable on light bg)
    "won":             QColor("#1a4d2e"),   # green dark
    "won_light":       QColor("#d4edda"),   # green light
    "lost":            QColor("#4d1a1a"),   # red dark
    "lost_light":      QColor("#f8d7da"),   # red light
    "draw":            QColor("#1a3a4d"),   # cyan dark
    "draw_light":      QColor("#d1ecf1"),   # cyan light
}


def _result_bg(result_int: int, dark: bool = True) -> QColor:
    """Return background QColor for a row given a numeric result."""
    suffix = "" if dark else "_light"
    if result_int == BetResult.PENDING:
        return _RESULT_COLORS["pending" + suffix] if not dark else _RESULT_COLORS[BetResult.PENDING]
    try:
        # We only know result here; profit sign determines won/lost/draw
        # Caller should use paint_row_items directly for full logic
        return QColor("transparent")
    except Exception:
        return QColor("transparent")


def paint_row_items(items: list, profit: float, result: int) -> None:
    """
    Apply background color to a list of QStandardItem objects based on
    bet result. The sport/bookie items (if marked with setData(True, SKIP_ROLE))
    are left untouched so their own background is preserved.
    """
    SKIP_ROLE = Qt.ItemDataRole.UserRole + 10

    if result == BetResult.PENDING:
        bg_dark  = QColor("#5a4d00")
        bg_light = QColor("#fff3cd")
    elif profit > 0:
        bg_dark  = QColor("#1a4d2e")
        bg_light = QColor("#c3e6cb")
    elif profit < 0:
        bg_dark  = QColor("#4d1a1a")
        bg_light = QColor("#f5c6cb")
    else:
        bg_dark  = QColor("#0d3040")
        bg_light = QColor("#bee5eb")

    for item in items:
        if item.data(SKIP_ROLE):
            continue
        item.setBackground(bg_dark)   # default; theme.py will override via QPalette if needed
        # Store light variant so themes can use it
        item.setData(bg_light, Qt.ItemDataRole.UserRole + 11)


def make_icon_item(icon_path: str | None, text: str, bg: QColor | None = None) -> QStandardItem:
    """
    Create a QStandardItem with optional icon and text.
    If icon_path exists, the icon is set. bg sets a custom background for this cell only.
    """
    SKIP_ROLE = Qt.ItemDataRole.UserRole + 10
    item = QStandardItem(text)
    item.setData(True, SKIP_ROLE)  # exclude from row-level paint
    if icon_path:
        pix = QPixmap(icon_path)
        if not pix.isNull():
            item.setIcon(QIcon(pix))
    if bg is not None:
        item.setBackground(bg)
    item.setEditable(False)
    return item


def make_item(text: str) -> QStandardItem:
    """Create a read-only QStandardItem."""
    item = QStandardItem(text)
    item.setEditable(False)
    return item


class BetconTableModel(QStandardItemModel):
    """QStandardItemModel subclass with helpers for Betcon tables."""

    def setup(self, headers: list[str], hidden_col: int = 1) -> None:
        """Configure column headers. hidden_col is the 0-based index of the ID column."""
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        self._hidden_col = hidden_col

    def get_id(self, row: int) -> str:
        """Return the ID stored in the hidden column for a given row."""
        item = self.item(row, self._hidden_col)
        return item.text() if item else ""
