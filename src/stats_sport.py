import sys, os, inspect
from PyQt5.QtWidgets import QWidget, QTreeWidgetItem
from PyQt5 import uic
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from libstats import LibStats
from func_aux import paint_row, key_from_value


class StatsSport(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/stats_sport.ui", self)
		self.mainWindows = mainWindows
		self.mainWindows.setWindowTitle("Estadisticas Deportes | Betcon v" + mainWindows.version)
		try:
			self.initData()
		except Exception:
			print("Error al intentar cargar los datos.")
			self.setEnabled(False)

		self.cmbYear.activated.connect(self.updateMonths)
		self.cmbMonth.activated.connect(self.updateTree)

	def initData(self):
		self.years, self.months = LibStats.getYears()
		self.cmbYear.addItems(self.years.keys())

		firstKey = next(iter(self.years))
		self.cmbMonth.addItems(self.getMonths(firstKey))

		data = LibStats.getSport()

		items = []
		for i in data:
			item = QTreeWidgetItem(i)
			item = paint_row(item, i[4])

			items.append(item)
		self.treeTotal.addTopLevelItems(items)

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

		data = LibStats.getSport(year, month)
		self.treeMonth.clear()

		items = []
		for i in data:
			item = QTreeWidgetItem(i)
			item = paint_row(item, i[4])
			items.append(item)
		self.treeMonth.addTopLevelItems(items)

	def getMonths(self, year):
		sMonths = []
		for i in self.years[year]:
			sMonths.append(self.months[i])
		return sMonths
