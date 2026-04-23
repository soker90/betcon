import os
from PySide6.QtCore import Qt, QObject, QEvent
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QApplication, QComboBox

_ASSETS = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "assets"))

_DARK = {
    "Window":          "#1e1e2e",
    "WindowText":      "#cdd6f4",
    "Base":            "#181825",
    "AlternateBase":   "#313244",
    "Text":            "#cdd6f4",
    "Button":          "#313244",
    "ButtonText":      "#cdd6f4",
    "BrightText":      "#f38ba8",
    "Highlight":       "#89b4fa",
    "HighlightedText": "#1e1e2e",
    "Link":            "#89dceb",
    "ToolTipBase":     "#45475a",
    "ToolTipText":     "#cdd6f4",
    "PlaceholderText": "#6c7086",
}

_LIGHT = {
    "Window":          "#f0f2f5",
    "WindowText":      "#1a1a2e",
    "Base":            "#ffffff",
    "AlternateBase":   "#eef0f5",
    "Text":            "#1a1a2e",
    "Button":          "#e0e3ea",
    "ButtonText":      "#1a1a2e",
    "BrightText":      "#c0392b",
    "Highlight":       "#0078d4",
    "HighlightedText": "#ffffff",
    "Link":            "#0078d4",
    "ToolTipBase":     "#fffbe6",
    "ToolTipText":     "#1a1a2e",
    "PlaceholderText": "#9e9e9e",
}

_ROLES = {
    "Window":          QPalette.ColorRole.Window,
    "WindowText":      QPalette.ColorRole.WindowText,
    "Base":            QPalette.ColorRole.Base,
    "AlternateBase":   QPalette.ColorRole.AlternateBase,
    "Text":            QPalette.ColorRole.Text,
    "Button":          QPalette.ColorRole.Button,
    "ButtonText":      QPalette.ColorRole.ButtonText,
    "BrightText":      QPalette.ColorRole.BrightText,
    "Highlight":       QPalette.ColorRole.Highlight,
    "HighlightedText": QPalette.ColorRole.HighlightedText,
    "Link":            QPalette.ColorRole.Link,
    "ToolTipBase":     QPalette.ColorRole.ToolTipBase,
    "ToolTipText":     QPalette.ColorRole.ToolTipText,
    "PlaceholderText": QPalette.ColorRole.PlaceholderText,
}


class _ComboHoverFilter(QObject):
    """Event filter that enables WA_Hover on every QComboBox view so that
    QSS ``::item:hover`` rules work correctly in popup mode."""

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.ChildAdded:
            child = event.child()
            if isinstance(child, QComboBox):
                child.view().setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        return False


_combo_hover_filter: _ComboHoverFilter | None = None


def _build_palette(colors: dict) -> QPalette:
    palette = QPalette()
    for name, hex_color in colors.items():
        role = _ROLES.get(name)
        if role is not None:
            palette.setColor(role, QColor(hex_color))
    return palette


def apply_theme(app: QApplication, mode: str = "dark") -> None:
    """Apply dark or light theme palette + QSS to the application."""
    global _combo_hover_filter

    colors = _DARK if mode == "dark" else _LIGHT
    app.setPalette(_build_palette(colors))

    qss_path = os.path.join(_ASSETS, f"{mode}.qss")
    if os.path.exists(qss_path):
        with open(qss_path, encoding="utf-8") as fh:
            qss = fh.read().replace("{ASSETS}", _ASSETS.replace("\\", "/"))
        app.setStyleSheet(qss)
    else:
        app.setStyleSheet("")

    # Install once: enables WA_Hover on QComboBox views so ::item:hover works.
    if _combo_hover_filter is None:
        _combo_hover_filter = _ComboHoverFilter()
        app.installEventFilter(_combo_hover_filter)

    # Also patch any comboboxes already alive.
    for combo in app.findChildren(QComboBox):
        combo.view().setAttribute(Qt.WidgetAttribute.WA_Hover, True)
