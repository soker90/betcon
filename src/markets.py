import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget, QTreeWidgetItem
from PyQt5 import uic, QtCore

directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from bbdd import Bbdd
from gettext import gettext as _
import gettext


class Markets(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/markets.ui", self)
		gettext.textdomain("betcon")
		gettext.bindtextdomain("betcon", "../lang/mo")
		gettext.bindtextdomain("betcon", "/usr/share/locale")
		self.mainWindows = mainWindows
		mainWindows.diconnectActions()
		mainWindows.aNew.triggered.connect(mainWindows.newMarket)
		self.mainWindows.setWindowTitle(_("Markets") + " | Betcon v" + mainWindows.version)
		self.treeMain.header().hideSection(1)
		self.initTree()

		self.treeMain.itemSelectionChanged.connect(self.changeItem)
		self.mainWindows.aEdit.triggered.connect(self.editItem)
		self.mainWindows.aRemove.triggered.connect(self.deleteItem)
		self.itemSelected = -1

		self.translate()

	def translate(self):

		header = [_("Name"), "index"]

		self.treeMain.setHeaderLabels(header)

	def initTree(self):
		bd = Bbdd()
		data = bd.select("market", "name")

		items = []
		for i in data:
			id = i[0]
			name = i[1]
			item = QTreeWidgetItem([name, str(id)])
			items.append(item)

		self.treeMain.addTopLevelItems(items)
		self.treeMain.sortByColumn(0, QtCore.Qt.AscendingOrder)

		bd.close()

	def changeItem(self):
		self.itemSelected = self.treeMain.currentItem().text(1)
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
			bd.deleteWhere("bet", "market=" + str(self.itemSelected))
			self.mainWindows.setCentralWidget(Markets(self.mainWindows))
			self.mainWindows.enableTools()

