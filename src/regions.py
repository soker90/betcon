import sys
import os
import inspect
from PySide6.QtWidgets import QMessageBox, QWidget, QAbstractItemView
from uiloader import loadUi
from table_model import BetconTableModel, make_item

directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from bbdd import Bbdd
from gettext import gettext as _
import gettext


class Regions(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		loadUi(directory + "/../ui/regions.ui", self)
		gettext.textdomain("betcon")
		gettext.bindtextdomain("betcon", "../lang/mo" + mainWindows.lang)
		gettext.bindtextdomain("betcon", "/usr/share/locale" + mainWindows.lang)
		self.mainWindows = mainWindows
		mainWindows.diconnectActions()
		mainWindows.aNew.triggered.connect(mainWindows.newRegion)
		self.mainWindows.setWindowTitle(_("Regions") + " | Betcon v" + mainWindows.version)
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
		header = [_("Name"), "index", _("Competitions")]

		self.model.setHorizontalHeaderLabels(header)

	def initTree(self):
		bd = Bbdd()
		self.model.removeRows(0, self.model.rowCount())
		data = bd.select("region", "name")
		for i in data:
			competitions = bd.count("competition", "region=" + str(i[0]))
			self.model.appendRow([make_item(i[1]), make_item(str(i[0])), make_item(str(competitions))])
		bd.close()

	def changeItem(self):
		indexes = self.treeMain.selectionModel().selectedRows()
		if not indexes:
			return
		self.itemSelected = self.model.get_id(indexes[0].row())
		self.mainWindows.enableActions()

	def editItem(self):
		self.mainWindows.editRegion(self.itemSelected)

	def deleteItem(self):
		resultado = QMessageBox.question(self, _("Remove"), _('Are you sure you want to eliminate the region ') +
		                                                    'and its associated competitions and bets?',
		                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if resultado == QMessageBox.Yes:
			bd = Bbdd()
			bd.delete("region", self.itemSelected)
			bd.deleteWhere("competition", "region=" + str(self.itemSelected))
			bd.deleteWhere("bet", "region=" + str(self.itemSelected))
			self.mainWindows.setCentralWidget(Regions(self.mainWindows))
			self.mainWindows.enableTools()
