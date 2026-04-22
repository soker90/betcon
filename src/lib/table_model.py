from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor, QIcon, QPixmap, QPainter
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QStyledItemDelegate
from constants import BetResult


def paint_row_items(items: list, profit: float, result: int) -> None:
    """
    Apply background color to a list of QStandardItem objects based on
    bet result. The sport/bookie items (if marked with setData(True, SKIP_ROLE))
    are left untouched so their own background is preserved.
    """
    SKIP_ROLE = Qt.ItemDataRole.UserRole + 10

    if result == BetResult.PENDING:
        bg = QColor(Qt.GlobalColor.yellow)
    elif profit > 0:
        bg = QColor(Qt.GlobalColor.green)
    elif profit < 0:
        bg = QColor(Qt.GlobalColor.red)
    else:
        bg = QColor(Qt.GlobalColor.cyan)

    for item in items:
        if item.data(SKIP_ROLE):
            continue
        item.setBackground(bg)


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


class BetconItemDelegate(QStyledItemDelegate):
    """
    Delegate that respects Qt.BackgroundRole on QStandardItems even when
    a QSS stylesheet is active (Qt normally ignores BackgroundRole when QSS
    sets background-color on the view).
    """

    def paint(self, painter: QPainter, option, index) -> None:
        bg = index.data(Qt.ItemDataRole.BackgroundRole)
        if bg is not None and bg.style() != Qt.BrushStyle.NoBrush:
            painter.save()
            painter.fillRect(option.rect, bg)
            painter.restore()
        super().paint(painter, option, index)
