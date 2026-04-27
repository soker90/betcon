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


class Markets(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		loadUi(directory + "/../ui/markets.ui", self)
		self.mainWindows = mainWindows
		mainWindows.diconnectActions()
		mainWindows.aNew.triggered.connect(mainWindows.newMarket)
		self.mainWindows.setWindowTitle(_("Markets") + " | Betcon v" + mainWindows.version)
		self.model = BetconTableModel()
		self.treeMain.setModel(self.model)
		self.treeMain.setAlternatingRowColors(True)
		self.treeMain.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
		self.treeMain.horizontalHeader().setStretchLastSection(True)
		self.treeMain.verticalHeader().setVisible(False)
		self.treeMain.setSortingEnabled(True)
		self.initTree()

		self.treeMain.selectionModel().selectionChanged.connect(self.changeItem)
		self.mainWindows.aEdit.triggered.connect(self.editItem)
		self.mainWindows.aRemove.triggered.connect(self.deleteItem)
		self.itemSelected = -1

		self.translate()
		self.treeMain.setColumnHidden(1, True)

	def translate(self):

		header = [_("Name"), "index"]

		self.model.setHorizontalHeaderLabels(header)

	def initTree(self):
		bd = Bbdd()
		self.model.removeRows(0, self.model.rowCount())
		data = bd.select("market", "name")
		for i in data:
			self.model.appendRow([make_item(i[1]), make_item(str(i[0]))])
		bd.close()

	def changeItem(self):
		indexes = self.treeMain.selectionModel().selectedRows()
		if not indexes:
			return
		self.itemSelected = self.model.get_id(indexes[0].row())
		self.mainWindows.enableActions()

	def editItem(self):
		self.mainWindows.editMarket(self.itemSelected)

	def deleteItem(self):
		resultado = QMessageBox.question(self, _("Remove"),
		                                 _("Are you sure you want to eliminate the market and the associated bets?"),
		                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if resultado == QMessageBox.Yes:
			bd = Bbdd()
			bd.delete("market", self.itemSelected)
			bd.deleteWhere("bet", "market=?", (self.itemSelected,))
			self.mainWindows.setCentralWidget(Markets(self.mainWindows))
			self.mainWindows.enableTools()

