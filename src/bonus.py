import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget, QTreeWidgetItem
from PyQt5 import uic
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from bbdd import Bbdd
from func_aux import str_to_bool
from gettext import gettext as _
import gettext
from libyaml import LibYaml


class Bonus(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/bonus.ui", self)
		gettext.textdomain("betcon")
		gettext.bindtextdomain("betcon", "../lang/mo")
		gettext.bindtextdomain("betcon", "/usr/share/locale")
		self.mainWindows = mainWindows
		mainWindows.diconnectActions()
		mainWindows.aNew.triggered.connect(mainWindows.newBonus)
		self.mainWindows.setWindowTitle(_("Bonus") + " | Betcon v" + mainWindows.version)
		self.treeMain.header().hideSection(1)

		self.coin = LibYaml().interface["coin"]
		self.initTree()

		self.treeMain.itemSelectionChanged.connect(self.changeItem)
		self.mainWindows.aEdit.triggered.connect(self.editItem)
		self.mainWindows.aRemove.triggered.connect(self.deleteItem)
		self.itemSelected = -1
		self.translate()

	def translate(self):

		header = [_("Date"), "index", _("Bookie"), _("Amount"), _("Freed")]

		self.treeMain.setHeaderLabels(header)


	def initTree(self):
		bd = Bbdd()
		data = bd.select("bonus", "date")

		items = []
		for i in data:
			id = i[0]
			date = i[1]
			bookie = bd.getValue(i[2], "bookie")
			money = i[3]
			free = _("Yes") if str_to_bool(i[4]) else _("No")
			item = QTreeWidgetItem([str(date), str(id), str(bookie), str(money) + self.coin, str(free)])
			items.append(item)

		self.treeMain.addTopLevelItems(items)

		bd.close()

	def changeItem(self):
		self.itemSelected = self.treeMain.currentItem().text(1)
		self.mainWindows.enableActions()

	def editItem(self):
		self.mainWindows.editBonus(self.itemSelected)

	def deleteItem(self):
		resultado = QMessageBox.question(self, _("Remove"), _("Are you sure you want to eliminate it?"), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if resultado == QMessageBox.Yes:
			bd = Bbdd()
			bd.delete("bonus", self.itemSelected)
			self.mainWindows.setCentralWidget(Bonus(self.mainWindows))
			self.mainWindows.enableTools()

