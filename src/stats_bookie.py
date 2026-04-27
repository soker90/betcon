import sys
import os
import inspect
from PySide6.QtWidgets import QWidget, QAbstractItemView
from uiloader import loadUi
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from libstats import LibStats
from func_aux import key_from_value
from table_model import BetconTableModel, make_item, paint_row_items


class StatsBookie(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		loadUi(directory + "/../ui/stats_bookie.ui", self)
		self.mainWindows = mainWindows
		self.mainWindows.setWindowTitle(_("Stats of bookies") + " | Betcon v" + mainWindows.version)
		self.translate()
		try:
			self.initData()
		except Exception:
			print(_("Error trying to load the data."))
			self.setEnabled(False)

		self.cmbYear.activated.connect(self.updateMonths)
		self.cmbMonth.activated.connect(self.updateTree)


	def translate(self):

		header = [_("Bookie"), _("Bets"), _("Success"), _("Money Bet"), _("Profits"), _("Stake"), _("Quota")]

		self.modelMonth = BetconTableModel()
		self.modelMonth.setup(header)
		self.treeMonth.setModel(self.modelMonth)
		self.treeMonth.setAlternatingRowColors(True)
		self.treeMonth.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
		self.treeMonth.horizontalHeader().setStretchLastSection(True)
		self.treeMonth.verticalHeader().setVisible(False)

		self.modelTotal = BetconTableModel()
		self.modelTotal.setup(header)
		self.treeTotal.setModel(self.modelTotal)
		self.treeTotal.setAlternatingRowColors(True)
		self.treeTotal.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
		self.treeTotal.horizontalHeader().setStretchLastSection(True)
		self.treeTotal.verticalHeader().setVisible(False)

		self.lblYear.setText(_("Year"))
		self.lblMonth.setText(_("Month"))
		self.lblTotalMonth.setText(_("Total of the month"))
		self.lblTotal.setText(_("Totals"))

	def initData(self):
		self.years, self.months = LibStats.getYears()
		self.cmbYear.addItems(self.years.keys())

		firstKey = next(iter(self.years))
		self.cmbMonth.addItems(self.getMonths(firstKey))

		data = LibStats.getBookie()

		for i in data:
			row = [make_item(str(v)) for v in i]
			profit_val = float(str(i[4]).rstrip('€$£ ').replace(',', '.') or '0')
			paint_row_items(row, profit_val, 1)
			self.modelTotal.appendRow(row)

		self.updateMonths()

	def updateMonths(self):
		year = self.cmbYear.currentText()
		self.cmbMonth.clear()
		self.cmbMonth.addItems(self.getMonths(year))
		self.updateTree()

	def updateTree(self):
		year = self.cmbYear.currentText()
		sMonth = self.cmbMonth.currentText()
		month = key_from_value(self.months, sMonth)

		data = LibStats.getBookie(year, month)
		self.modelMonth.removeRows(0, self.modelMonth.rowCount())

		for i in data:
			row = [make_item(str(v)) for v in i]
			profit_val = float(str(i[4]).rstrip('€$£ ').replace(',', '.') or '0')
			paint_row_items(row, profit_val, 1)
			self.modelMonth.appendRow(row)

	def getMonths(self, year):
		sMonths = []
		for i in self.years[year]:
			sMonths.append(self.months[i])
		return sMonths
