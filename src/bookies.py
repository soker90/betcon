import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget, QTreeWidgetItem
from PyQt5 import uic, QtCore

directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
from bookie import Bookie
from gettext import gettext as _
import gettext

class Bookies(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/bookies.ui", self)
		gettext.textdomain("betcon")
		gettext.bindtextdomain("betcon", "../lang/mo" + mainWindows.lang)
		gettext.bindtextdomain("betcon", "/usr/share/locale" + mainWindows.lang)
		self.mainWindows = mainWindows
		mainWindows.diconnectActions()
		mainWindows.aNew.triggered.connect(mainWindows.newBookie)
		self.mainWindows.setWindowTitle(_("Bookies") + " | Betcon v" + mainWindows.version)
		self.treeMain.header().hideSection(1)
		self.initTree()
		self.treeMain.itemSelectionChanged.connect(self.changeItem)
		self.mainWindows.aEdit.triggered.connect(self.editItem)
		self.mainWindows.aRemove.triggered.connect(self.deleteItem)

		self.itemSelected = -1

		self.translate()

	def translate(self):

		header = [_("Name"), "index", _("Country")]

		self.treeMain.setHeaderLabels(header)

	def initTree(self):
		data = Bookie.selectAll()

		items = []
		for i in data:
			item = QTreeWidgetItem([i.name, str(i.id), i.country])
			items.append(item)

		self.treeMain.addTopLevelItems(items)
		self.treeMain.sortByColumn(0, QtCore.Qt.AscendingOrder)


	def changeItem(self):
		self.itemSelected = self.treeMain.currentItem().text(1)
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

