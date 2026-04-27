"""Qt UI Translation Helper"""
from PySide6.QtWidgets import QWidget, QMenu, QLabel, QPushButton, QTabWidget
from PySide6.QtWidgets import QGroupBox, QCheckBox, QRadioButton
from PySide6.QtGui import QAction

def translate_widget(widget):
    """Recursively translate all child widgets"""
    # Translate the widget itself
    if hasattr(widget, 'text'):
        try:
            original = widget.text()
            if original:
                translated = _(original)
                if translated != original:
                    widget.setText(translated)
        except:
            pass
    
    # Translate window title
    if hasattr(widget, 'windowTitle'):
        try:
            original = widget.windowTitle()
            if original and original != 'MainWindow':
                translated = _(original)
                if translated != original:
                    widget.setWindowTitle(translated)
        except:
            pass
    
    # Translate placeholderText for line edits
    if hasattr(widget, 'placeholderText'):
        try:
            original = widget.placeholderText()
            if original:
                translated = _(original)
                if translated != original:
                    widget.setPlaceholderText(translated)
        except:
            pass
    
    # Translate tooltips
    if hasattr(widget, 'toolTip'):
        try:
            original = widget.toolTip()
            if original:
                translated = _(original)
                if translated != original:
                    widget.setToolTip(translated)
        except:
            pass
    
    # Translate tab titles
    if isinstance(widget, QTabWidget):
        for i in range(widget.count()):
            original = widget.tabText(i)
            if original:
                translated = _(original)
                if translated != original:
                    widget.setTabText(i, translated)
    
    # Translate menu and action text
    if isinstance(widget, QMenu):
        original = widget.title()
        if original:
            translated = _(original)
            if translated != original:
                widget.setTitle(translated)
    
    if isinstance(widget, QAction):
        original = widget.text()
        if original:
            translated = _(original)
            if translated != original:
                widget.setText(translated)
    
    # Recursively translate children
    if hasattr(widget, 'children'):
        for child in widget.children():
            if isinstance(child, QWidget):
                translate_widget(child)
