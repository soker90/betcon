import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src", "lib"))

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor
from theme import apply_theme, _build_palette, _DARK, _LIGHT


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    yield app


def test_apply_dark_theme_does_not_raise(qapp):
    apply_theme(qapp, "dark")


def test_apply_light_theme_does_not_raise(qapp):
    apply_theme(qapp, "light")


def test_apply_unknown_mode_falls_back_to_light(qapp):
    # Unknown mode defaults to light (mode != "dark")
    apply_theme(qapp, "unknown")


def test_dark_palette_window_color():
    palette = _build_palette(_DARK)
    expected = QColor("#1e1e2e")
    assert palette.color(QPalette.ColorRole.Window) == expected


def test_light_palette_window_color():
    palette = _build_palette(_LIGHT)
    expected = QColor("#f0f2f5")
    assert palette.color(QPalette.ColorRole.Window) == expected


def test_dark_palette_highlight():
    palette = _build_palette(_DARK)
    expected = QColor("#89b4fa")
    assert palette.color(QPalette.ColorRole.Highlight) == expected


def test_light_palette_highlight():
    palette = _build_palette(_LIGHT)
    expected = QColor("#0078d4")
    assert palette.color(QPalette.ColorRole.Highlight) == expected


def test_qss_file_applied_dark(qapp):
    apply_theme(qapp, "dark")
    # If the QSS file exists, stylesheet should be non-empty
    qss_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "assets", "dark.qss"
    )
    if os.path.exists(qss_path):
        assert len(qapp.styleSheet()) > 0


def test_qss_file_applied_light(qapp):
    apply_theme(qapp, "light")
    qss_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "assets", "light.qss"
    )
    if os.path.exists(qss_path):
        assert len(qapp.styleSheet()) > 0
