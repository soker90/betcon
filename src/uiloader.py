from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice
from lib.qt_translator import translate_widget
import os


class _UiLoader(QUiLoader):
	"""Subclass that loads a .ui file directly into an existing widget instance,
	replicating the behaviour of PyQt5's loadUi(path, base_instance)."""

	def __init__(self, base_instance):
		super().__init__(base_instance)
		self._base = base_instance

	def createWidget(self, class_name, parent=None, name=""):
		# When creating the root widget (no parent), return the existing instance
		# so all child widgets are reparented into it.
		if parent is None and self._base is not None:
			return self._base
		return super().createWidget(class_name, parent, name)


def loadUi(ui_file, base_instance=None):
	"""Load a Qt Designer .ui file into base_instance (or return a new widget)."""
	# Normalize the path to handle cases like /path/src/../ui/file.ui
	# where 'src' doesn't exist but ../ui should still resolve correctly
	ui_file_normalized = os.path.normpath(ui_file)
	
	loader = _UiLoader(base_instance)
	f = QFile(ui_file_normalized)
	f.open(QIODevice.OpenModeFlag.ReadOnly)
	widget = loader.load(f)
	f.close()
	# Automatically translate all widgets
	translate_widget(widget)
	return widget
