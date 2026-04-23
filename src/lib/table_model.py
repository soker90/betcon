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
    has_icon = False
    if icon_path:
        pix = QPixmap(icon_path)
        if not pix.isNull():
            has_icon = True
    item = QStandardItem("" if has_icon else text)
    item.setData(True, SKIP_ROLE)  # exclude from row-level paint
    if has_icon:
        item.setIcon(QIcon(pix))
        item.setToolTip(text)
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._hidden_col = 1

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
    Delegate that:
    1. Respects Qt.BackgroundRole even when a QSS stylesheet is active.
    2. Scales icon-only cells (empty text, has icon) to fill the whole cell rect.
    3. Applies a row-wide hover highlight.
    """

    _ICON_ROLE = Qt.ItemDataRole.DecorationRole
    _TEXT_ROLE = Qt.ItemDataRole.DisplayRole

    def __init__(self, parent=None):
        super().__init__(parent)
        self._hovered_row = -1

    def set_hovered_row(self, row: int) -> None:
        self._hovered_row = row

    def paint(self, painter: QPainter, option, index) -> None:
        # 1. Paint custom background
        bg = index.data(Qt.ItemDataRole.BackgroundRole)
        if bg is not None and bg.style() != Qt.BrushStyle.NoBrush:
            painter.save()
            painter.fillRect(option.rect, bg)
            painter.restore()

        # 2. If icon-only cell, draw icon scaled to fill the cell
        text = index.data(self._TEXT_ROLE) or ""
        icon = index.data(self._ICON_ROLE)
        if icon and not text:
            painter.save()
            pixmap = icon.pixmap(option.rect.size())
            painter.drawPixmap(option.rect, pixmap)
            painter.restore()
        else:
            super().paint(painter, option, index)

        # 3. Row-wide hover overlay (drawn last, on top)
        if index.row() == self._hovered_row:
            painter.save()
            painter.fillRect(option.rect, QColor(255, 255, 255, 40))
            painter.restore()
