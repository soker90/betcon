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


class Competitions(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		loadUi(directory + "/../ui/competitions.ui", self)
		self.mainWindows = mainWindows
		mainWindows.diconnectActions()
		self.model = BetconTableModel()
		self.treeMain.setModel(self.model)
		self.treeMain.setAlternatingRowColors(True)
		self.treeMain.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
		self.treeMain.horizontalHeader().setStretchLastSection(True)
		self.treeMain.verticalHeader().setVisible(False)
		self.treeMain.setSortingEnabled(True)
		mainWindows.aNew.triggered.connect(mainWindows.newCompetition)
		self.mainWindows.setWindowTitle(_("Competitions") + " | Betcon v" + mainWindows.version)
		self.initTree()
		self.treeMain.selectionModel().selectionChanged.connect(self.changeItem)
		self.mainWindows.aEdit.triggered.connect(self.editItem)
		self.mainWindows.aRemove.triggered.connect(self.deleteItem)
		self.itemSelected = -1
		self.translate()
		self.treeMain.setColumnHidden(1, True)

	def translate(self):

		header = [_("Name"), "index", _("Region"), _("Sport")]

		self.model.setHorizontalHeaderLabels(header)

	def initTree(self):
		bd = Bbdd()
		self.model.removeRows(0, self.model.rowCount())
		data = bd.select("competition", "name")
		for i in data:
			region = bd.getValue(i[2], "region") or ""
			sport = bd.getValue(i[3], "sport") or ""
			self.model.appendRow([make_item(str(i[1])), make_item(str(i[0])), make_item(region), make_item(str(sport))])
		bd.close()

	def changeItem(self):
		indexes = self.treeMain.selectionModel().selectedRows()
		if not indexes:
			return
		self.itemSelected = self.model.get_id(indexes[0].row())
		self.mainWindows.enableActions()

	def editItem(self):
		self.mainWindows.editCompetition(self.itemSelected)

	def deleteItem(self):
		resultado = QMessageBox.question(self, _("Remove"), _("Are you sure you want to eliminate ") +
		                                 _("the competition and the associated bets?"), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if resultado == QMessageBox.Yes:
			bd = Bbdd()
			bd.delete("competition", self.itemSelected)
			bd.deleteWhere("bet", "competition=?", (self.itemSelected,))
			self.mainWindows.setCentralWidget(Competitions(self.mainWindows))
			self.mainWindows.enableTools()



