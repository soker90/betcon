import sys
import os
from lib.paths import get_base_dir
import inspect
from PySide6.QtWidgets import QMessageBox, QWidget, QAbstractItemView
from uiloader import loadUi
from table_model import BetconTableModel, make_item
directory = get_base_dir()
sys.path.append(directory + "/lib")
from bbdd import Bbdd
from func_aux import str_to_bool
from libyaml import LibYaml


class Bonus(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		loadUi(directory + "/../ui/bonus.ui", self)
		self.mainWindows = mainWindows
		mainWindows.diconnectActions()
		mainWindows.aNew.triggered.connect(mainWindows.newBonus)
		self.mainWindows.setWindowTitle(_("Bonus") + " | Betcon v" + mainWindows.version)
		self.model = BetconTableModel()
		self.treeMain.setModel(self.model)
		self.treeMain.setAlternatingRowColors(True)
		self.treeMain.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
		self.treeMain.horizontalHeader().setStretchLastSection(True)
		self.treeMain.verticalHeader().setVisible(False)
		self.treeMain.setSortingEnabled(True)

		self.coin = LibYaml().interface["coin"]
		self.initTree()

		self.treeMain.selectionModel().selectionChanged.connect(self.changeItem)
		self.mainWindows.aEdit.triggered.connect(self.editItem)
		self.mainWindows.aRemove.triggered.connect(self.deleteItem)
		self.itemSelected = -1
		self.translate()
		self.treeMain.setColumnHidden(1, True)

	def translate(self):

		header = [_("Date"), "index", _("Bookie"), _("Amount"), _("Freed")]

		self.model.setHorizontalHeaderLabels(header)


	def initTree(self):
		bd = Bbdd()
		self.model.removeRows(0, self.model.rowCount())
		data = bd.select("bonus", "date")
		for i in data:
			bookie = bd.getValue(i[2], "bookie") or ""
			free = _("Yes") if str_to_bool(i[4]) else _("No")
			self.model.appendRow([make_item(str(i[1])), make_item(str(i[0])), make_item(str(bookie)), make_item(str(i[3]) + self.coin), make_item(free)])

		bd.close()

	def changeItem(self):
		indexes = self.treeMain.selectionModel().selectedRows()
		if not indexes:
			return
		self.itemSelected = self.model.get_id(indexes[0].row())
		self.mainWindows.enableActions()

	def editItem(self):
		self.mainWindows.editBonus(self.itemSelected)

	def deleteItem(self):
		msg = QMessageBox(self)
		msg.setWindowTitle(_("Remove"))
		msg.setText(_("Are you sure you want to eliminate it?"))
		msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
		msg.setDefaultButton(QMessageBox.No)
		msg.setButtonText(QMessageBox.Yes, _("Yes"))
		msg.setButtonText(QMessageBox.No, _("No"))
		resultado = msg.exec()
		if resultado == QMessageBox.Yes:
			bd = Bbdd()
			bd.delete("bonus", self.itemSelected)
			self.mainWindows.setCentralWidget(Bonus(self.mainWindows))
			self.mainWindows.enableTools()

