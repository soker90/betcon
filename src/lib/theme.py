import os
import re
import subprocess
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QApplication

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


def _build_palette(colors: dict) -> QPalette:
    palette = QPalette()
    for name, hex_color in colors.items():
        role = _ROLES.get(name)
        if role is not None:
            palette.setColor(role, QColor(hex_color))
    return palette


_requested_mode: str = "auto"
_scheme_signal_connected: bool = False


def _detect_os_dark_linux() -> "bool | None":
    """Detect dark mode on Linux using freedesktop sources. Returns ``None``
    when no source can answer.
    """
    # 1) xdg-desktop-portal Settings (works on GNOME, KDE, Wayland).
    try:
        out = subprocess.run(
            [
                "gdbus", "call", "--session",
                "--dest", "org.freedesktop.portal.Desktop",
                "--object-path", "/org/freedesktop/portal/desktop",
                "--method", "org.freedesktop.portal.Settings.Read",
                "org.freedesktop.appearance", "color-scheme",
            ],
            capture_output=True, text=True, timeout=1,
        )
        if out.returncode == 0 and out.stdout:
            # Returns e.g. "(<<uint32 1>>,)"  where 1=dark, 2=light, 0=no preference.
            match = re.search(r"uint32\s+(\d+)", out.stdout)
            if match:
                value = int(match.group(1))
                if value == 1:
                    return True
                if value == 2:
                    return False
    except Exception:
        pass
    # 2) GNOME / GTK gsettings.
    for key in ("color-scheme", "gtk-theme"):
        try:
            out = subprocess.run(
                ["gsettings", "get", "org.gnome.desktop.interface", key],
                capture_output=True, text=True, timeout=1,
            )
            if out.returncode == 0 and out.stdout:
                value = out.stdout.strip().strip("'").lower()
                if "dark" in value:
                    return True
                if value in ("default", "prefer-light") or "light" in value:
                    return False
        except Exception:
            pass
    # 3) KDE kdeglobals.
    try:
        kde = os.path.expanduser("~/.config/kdeglobals")
        if os.path.exists(kde):
            with open(kde, encoding="utf-8", errors="ignore") as fh:
                for line in fh:
                    if line.lower().startswith("colorscheme"):
                        return "dark" in line.lower()
    except Exception:
        pass
    return None


def _detect_os_dark(app: QApplication) -> bool:
    """Return ``True`` if the host OS is currently using a dark color scheme."""
    try:
        scheme = app.styleHints().colorScheme()
        if scheme == Qt.ColorScheme.Dark:
            return True
        if scheme == Qt.ColorScheme.Light:
            # On Linux many platform plugins always report Light; double-check.
            linux_dark = _detect_os_dark_linux()
            if linux_dark is not None:
                return linux_dark
            return False
    except Exception:
        pass
    linux_dark = _detect_os_dark_linux()
    if linux_dark is not None:
        return linux_dark
    win = app.palette().color(QPalette.ColorRole.Window)
    return win.lightnessF() < 0.5


def _resolve_mode(mode: str, app: QApplication) -> str:
    """Translate ``"auto"`` to ``"dark"`` / ``"light"`` based on the host OS."""
    if mode != "auto":
        return mode
    return "dark" if _detect_os_dark(app) else "light"


def _on_color_scheme_changed(_scheme=None) -> None:
    app = QApplication.instance()
    if app is None or _requested_mode != "auto":
        return
    _apply(app, _requested_mode)


def _apply(app: QApplication, mode: str) -> None:
    effective = _resolve_mode(mode, app)
    colors = _DARK if effective == "dark" else _LIGHT
    app.setPalette(_build_palette(colors))

    qss_path = os.path.join(_ASSETS, f"{effective}.qss")
    if os.path.exists(qss_path):
        with open(qss_path, encoding="utf-8") as fh:
            qss = fh.read().replace("{ASSETS}", _ASSETS.replace("\\", "/"))
        app.setStyleSheet(qss)
    else:
        app.setStyleSheet("")


def apply_theme(app: QApplication, mode: str = "auto") -> None:
    """Apply dark, light or auto theme palette + QSS to the application.

    ``auto`` follows the operating system color scheme and updates the app
    automatically when the OS scheme changes. Uses the platform's native Qt
    style so widgets blend with the host OS.
    """
    global _requested_mode, _scheme_signal_connected
    _requested_mode = mode if mode in ("auto", "dark", "light") else "auto"

    if not _scheme_signal_connected:
        try:
            app.styleHints().colorSchemeChanged.connect(_on_color_scheme_changed)
            _scheme_signal_connected = True
        except Exception:
            pass

    _apply(app, _requested_mode)
