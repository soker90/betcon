import sys, os, inspect
from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QMessageBox, QTreeWidget
from PyQt5.QtGui import QBrush, QPixmap, QFont
from PyQt5.QtCore import Qt, QStringListModel
from PyQt5 import uic
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from bbdd import Bbdd
from func_aux import numberToResult, paint_row
from gettext import gettext as _
import gettext


class Bets(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/bets.ui", self)
		gettext.textdomain("betcon")
		gettext.bindtextdomain("betcon", "../lang/mo")
		self.mainWindows = mainWindows
		mainWindows.diconnectActions()
		mainWindows.aNew.triggered.connect(mainWindows.newBet)
		self.mainWindows.setWindowTitle(_("Home") + " | Betcon v" + mainWindows.version)
		self.treeMain.header().hideSection(1)
		self.initTree()
		self.treeMain.itemSelectionChanged.connect(self.changeItem)
		self.mainWindows.aEdit.triggered.connect(self.editItem)
		self.mainWindows.aRemove.triggered.connect(self.deleteItem)

		self.itemSelected = -1
		self.indexSelected = -1

		header = [" ", "index", _("Date"), _("Sport"), _("Competition"), _("Region"), _("Local Team"), _("Away Team"),
		          _("Pick"), _("Bookie"), _("Market"), _("Tipster"), _("Stake"), _("Stake 1"), _("Bet"), _("Quota"),
		          _("Result"), _("Profit")]

		self.treeMain.setHeaderLabels(header)

	def initTree(self):
		bd = Bbdd()
		data = bd.select("bet", "date DESC")

		index = 0
		items = []
		for i in data:
			index += 1
			id = i[0]
			date = i[1]
			competition = bd.getValue(i[3], "competition")
			region = bd.getValue(i[4], "region")
			player1 = i[5]
			player2 = i[6]
			pick = i[7]
			#bookie = bd.getValue(i[8], "bookie")
			market = bd.getValue(i[9], "market")  # TODO Preload in dictionary
			tipster = bd.getValue(i[10], "tipster")  # TODO Preload in dictionary
			stake = i[11]
			one = i[12]
			result = numberToResult(i[13])
			profit = i[14]
			bet = i[15]
			quota = i[16]

			item = QTreeWidgetItem([str(index), str(id), str(date), "", str(competition), str(region), player1,
									player2, pick, "", market, tipster, str(stake), str(one), str(bet), str(quota),
									str(result), str(profit)])

			item = paint_row(item, profit, result)


			if os.path.isfile(directory + "/../resources/sports/" + str(i[2]) + ".png"):
				item.setBackground(3, QBrush(QPixmap(directory + "/../resources/sports/" + str(i[2]) + ".png")))
			else:
				sport = bd.getValue(i[2], "sport")
				item.setText(3, sport)

			if os.path.isfile(directory + "/../resources/bookies/" + str(i[8]) + ".png"):
				item.setBackground(9, QBrush(QPixmap(directory + "/../resources/bookies/" + str(i[8]) + ".png")))
			else:
				bookie = bd.getValue(i[8], "bookie")
				item.setText(9, bookie)

			items.append(item)

		self.treeMain.addTopLevelItems(items)

		bd.close()

	def changeItem(self):

		if self.itemSelected != -1:
			self.treeMain.topLevelItem(self.indexSelected).setText(3, "")
			self.treeMain.topLevelItem(self.indexSelected).setText(9, "")

		self.itemSelected = self.treeMain.currentItem().text(1)
		self.indexSelected = int(self.treeMain.currentItem().text(0)) - 1

		bd = Bbdd()
		sport = bd.getValue(self.treeMain.currentItem().text(1), "bet", "sport")
		sport = bd.getValue(sport, "sport")
		self.treeMain.currentItem().setText(3, sport)

		bookie = bd.getValue(self.treeMain.currentItem().text(1), "bet", "bookie")
		bookie = bd.getValue(bookie, "bookie")
		self.treeMain.currentItem().setText(9, bookie)
		bd.close()
		self.mainWindows.enableActions()

	def editItem(self):
		self.mainWindows.editBet(self.itemSelected)

	def deleteItem(self):
		resultado = QMessageBox.question(self, _("Remove"), _("Are you sure you want to eliminate it?"),
										 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if resultado == QMessageBox.Yes:
			bd = Bbdd()
			bd.delete("bet", self.itemSelected)
			bd.deleteWhere("combined", "bet=" + str(self.itemSelected))
			self.mainWindows.setCentralWidget(Bets(self.mainWindows))
			self.mainWindows.enableTools()






