import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget, QTreeWidgetItem
from PyQt5 import uic

directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")

from bbdd import Bbdd
from func_aux import numberToMonth
from gettext import gettext as _
import gettext
from libyaml import LibYaml


class TipstersMonth(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/tipsters_month.ui", self)
		gettext.textdomain("betcon")
		gettext.bindtextdomain("betcon", "../lang/mo")
		gettext.bindtextdomain("betcon", "/usr/share/locale")
		self.mainWindows = mainWindows
		mainWindows.aNew.triggered.connect(mainWindows.newTipsterMonth)
		self.mainWindows.setWindowTitle(_("Tipsters - Payment history") + " | Betcon v" + mainWindows.version)
		self.treeMain.header().hideSection(0)
		self.treeConjunta.header().hideSection(0)

		self.coin = LibYaml().interface["coin"]

		self.translate()
		self.initTree()

		self.treeMain.itemSelectionChanged.connect(self.changeItem)
		self.treeConjunta.itemSelectionChanged.connect(self.changeItemConjunta)
		self.mainWindows.aEdit.triggered.connect(self.editItem)
		self.mainWindows.aRemove.triggered.connect(self.deleteItem)
		self.mainWindows.enableActionConjunta(False)
		self.mainWindows.aEditConjunta.triggered.connect(self.editConjunta)
		self.mainWindows.aDeleteConjunta.triggered.connect(self.deleteConjunta)
		self.itemSelected = -1
		self.itemConjunta = -1

	def translate(self):

		header = ["index", _("Year"), _("Month"), _("Tipster"), _("Cost")]

		self.treeMain.setHeaderLabels(header)
		self.treeConjunta.setHeaderLabels(header)
		self.lblConjunta.setText(_("Joint purchase"))

	def initTree(self):
		bd = Bbdd()
		data = bd.select("tipster_month", "year, month")

		items = []
		for i in data:
			id = i[0]
			year = i[2]
			month = numberToMonth(i[1]+1)
			tipster = bd.getValue(i[3], "tipster")
			money = i[4]
			item = QTreeWidgetItem([str(id), str(year), str(month), str(tipster), str(money) + self.coin])
			items.append(item)

		self.treeMain.addTopLevelItems(items)

		data = bd.select("conjunta", "year, month")

		if len(data) < 1:
			self.lblConjunta.setVisible(False)
			self.treeConjunta.setVisible(False)
		else:
			items = []
			for i in data:
				id = i[0]
				year = i[3]
				month = numberToMonth(i[2] + 1)
				name = i[1]
				money = i[4]
				item = QTreeWidgetItem([str(id), str(year), str(month), str(name), str(money) + self.coin])
				items.append(item)

			self.treeConjunta.addTopLevelItems(items)

		bd.close()

	def changeItem(self):
		self.itemSelected = self.treeMain.currentItem().text(0)
		self.mainWindows.enableActions()

	def changeItemConjunta(self):
		self.itemConjunta = self.treeConjunta.currentItem().text(0)
		self.mainWindows.enableActionConjunta(True)

	def editItem(self):
		self.mainWindows.editTipsterMonth(self.itemSelected)

	def editConjunta(self):
		self.mainWindows.editConjunta(self.itemConjunta)

	def deleteItem(self):
		resultado = QMessageBox.question(self, _("Remove"),
		                                 _("Are you sure you want to eliminate this payment?"),
		                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if resultado == QMessageBox.Yes:
			bd = Bbdd()
			bd.delete("tipster_month", self.itemSelected)
			self.mainWindows.setCentralWidget(TipstersMonth(self.mainWindows))
			self.mainWindows.enableTools("tipster_money")
			bd.close()

	def deleteConjunta(self):
		resultado = QMessageBox.question(self, _("Remove"),
		                                 _("Are you sure you want to eliminate this purchase joint?"),
		                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if resultado == QMessageBox.Yes:
			bd = Bbdd()
			bd.delete("conjunta", str(self.itemConjunta))
			bd.deleteWhere("conjunta_tipster","conjunta=" + str(self.itemConjunta))
			self.mainWindows.setCentralWidget(TipstersMonth(self.mainWindows))
			self.mainWindows.enableTools("tipster_money")
			bd.close()

