import os
import inspect
from PySide6.QtWidgets import QMessageBox, QWidget, QTreeWidgetItem
from PySide6 import QtCore
from uiloader import loadUi

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
		self.treeMain.sortByColumn(0, QtCore.Qt.SortOrder.AscendingOrder)


	def changeItem(self):
              current = self.treeMain.currentItem()
              if current is None:
                      return
              self.itemSelected = current.text(1)

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

