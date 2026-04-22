import os
import inspect
from PySide6.QtWidgets import QMessageBox, QWidget, QAbstractItemView
from uiloader import loadUi
from table_model import BetconTableModel, make_item

directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
from bookie import Bookie
from gettext import gettext as _
import gettext

class Bookies(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		loadUi(directory + "/../ui/bookies.ui", self)
		gettext.textdomain("betcon")
		gettext.bindtextdomain("betcon", "../lang/mo" + mainWindows.lang)
		gettext.bindtextdomain("betcon", "/usr/share/locale" + mainWindows.lang)
		self.mainWindows = mainWindows
		mainWindows.diconnectActions()
		mainWindows.aNew.triggered.connect(mainWindows.newBookie)
		self.mainWindows.setWindowTitle(_("Bookies") + " | Betcon v" + mainWindows.version)
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

		header = [_("Name"), "index", _("Country")]

		self.model.setHorizontalHeaderLabels(header)

	def initTree(self):
		data = Bookie.selectAll()
		self.model.removeRows(0, self.model.rowCount())
		for i in data:
			self.model.appendRow([make_item(i.name), make_item(str(i.id)), make_item(i.country)])

	def changeItem(self):
		indexes = self.treeMain.selectionModel().selectedRows()
		if not indexes:
			return
		self.itemSelected = self.model.get_id(indexes[0].row())
		self.mainWindows.enableActions()

	def editItem(self):
		self.mainWindows.editBookie(self.itemSelected)

	def deleteItem(self):
		resultado = QMessageBox.question(self, _("Remove"), _("Are you sure you want to eliminate the bookie and the associated bets?"),
										 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if resultado == QMessageBox.Yes:
			err = Bookie.delete(self.itemSelected)
			Bookie.deleteWhere("bet", "bookie=" + str(self.itemSelected))
			Bookie.deleteWhere("bonus", "bookie=" + str(self.itemSelected))
			if err != 0:
				QMessageBox.critical(self, _("Error"), _("There was an error deleting the house"))

			self.mainWindows.setCentralWidget(Bookies(self.mainWindows))
			self.mainWindows.enableTools()

