import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget, QTreeWidgetItem
from PyQt5 import uic, QtCore

directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")

from bbdd import Bbdd
from gettext import gettext as _
import gettext


class Competitions(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/competitions.ui", self)
		gettext.textdomain("betcon")
		gettext.bindtextdomain("betcon", "../lang/mo" + mainWindows.lang)
		gettext.bindtextdomain("betcon", "/usr/share/locale" + mainWindows.lang)
		self.mainWindows = mainWindows
		mainWindows.diconnectActions()
		self.treeMain.header().hideSection(1)
		mainWindows.aNew.triggered.connect(mainWindows.newCompetition)
		self.mainWindows.setWindowTitle(_("Competitions") + " | Betcon v" + mainWindows.version)
		self.initTree()
		self.treeMain.itemSelectionChanged.connect(self.changeItem)
		self.mainWindows.aEdit.triggered.connect(self.editItem)
		self.mainWindows.aRemove.triggered.connect(self.deleteItem)
		self.itemSelected = -1
		self.translate()

	def translate(self):

		header = [_("Name"), "index", _("Region"), _("Sport")]

		self.treeMain.setHeaderLabels(header)

	def initTree(self):
		bd = Bbdd()
		data = bd.select("competition", "name")

		items = []
		for i in data:
			id = i[0]
			name = i[1]
			region = bd.getValue(i[2], "region")
			sport = bd.getValue(i[3], "sport")
			item = QTreeWidgetItem([str(name), str(id), region, str(sport)])
			items.append(item)

		self.treeMain.addTopLevelItems(items)
		self.treeMain.sortByColumn(0, QtCore.Qt.AscendingOrder)

		bd.close()

	def changeItem(self):
		self.itemSelected = self.treeMain.currentItem().text(1)
		self.mainWindows.enableActions()

	def editItem(self):
		self.mainWindows.editCompetition(self.itemSelected)

	def deleteItem(self):
		resultado = QMessageBox.question(self, _("Remove"), _("Are you sure you want to eliminate ") +
		                                 _("the competition and the associated bets?"), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if resultado == QMessageBox.Yes:
			bd = Bbdd()
			bd.delete("competition", self.itemSelected)
			bd.deleteWhere("bet", "competition=" + str(self.itemSelected))
			self.mainWindows.setCentralWidget(Competitions(self.mainWindows))
			self.mainWindows.enableTools()



