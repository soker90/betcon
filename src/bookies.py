import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget, QTreeWidgetItem
from PyQt5 import uic
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
from bookie import Bookie
from gettext import gettext as _
import gettext

class Bookies(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/bookies.ui", self)
		gettext.textdomain("betcon")
		gettext.bindtextdomain("betcon", "../lang/mo")
		self.mainWindows = mainWindows
		mainWindows.diconnectActions()
		mainWindows.aNew.triggered.connect(mainWindows.newBookie)
		self.mainWindows.setWindowTitle(_("Casas de apuestas") + " | Betcon v" + mainWindows.version)
		self.treeMain.header().hideSection(1)
		self.initTree()
		self.treeMain.itemSelectionChanged.connect(self.changeItem)
		self.mainWindows.aEdit.triggered.connect(self.editItem)
		self.mainWindows.aRemove.triggered.connect(self.deleteItem)

		self.itemSelected = -1

	def initTree(self):
		data = Bookie.selectAll()

		index = 0
		items = []
		for i in data:
			index += 1
			item = QTreeWidgetItem([str(index), str(i.id), i.name])
			items.append(item)

		self.treeMain.addTopLevelItems(items)


	def changeItem(self):
		self.itemSelected = self.treeMain.currentItem().text(1)
		self.mainWindows.enableActions() if int(self.itemSelected) > 7 else self.mainWindows.enableTools()

	def editItem(self):
		self.mainWindows.editBookie(self.itemSelected)

	def deleteItem(self):
		resultado = QMessageBox.question(self, _("Eliminar"), _("¿Estas seguro que desas eliminar la casa y las apuestas asociadas?"),
										 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if resultado == QMessageBox.Yes:
			err = Bookie.delete(self.itemSelected)
			Bookie.deleteWhere("bet", "bookie=" + str(self.itemSelected))
			Bookie.deleteWhere("bonus", "bookie=" + str(self.itemSelected))
			if err != 0:
				QMessageBox.critical(self, _("Error"), _("Se ha producido un error al borrar la casa"))

			self.mainWindows.setCentralWidget(Bookies(self.mainWindows))
			self.mainWindows.enableTools()

