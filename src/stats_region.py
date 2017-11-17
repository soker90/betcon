import sys, os, inspect
from PyQt5.QtWidgets import QWidget, QTreeWidgetItem
from PyQt5 import uic
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from libstats import LibStats
from func_aux import paint_row, key_from_value
from gettext import gettext as _
import gettext


class StatsRegion(QWidget):
    def __init__(self, mainWindows):
        QWidget.__init__(self)
        uic.loadUi(directory + "/../ui/stats_region.ui", self)
        gettext.textdomain("betcon")
        gettext.bindtextdomain("betcon", "../lang/mo")
        self.mainWindows = mainWindows
        self.mainWindows.setWindowTitle(_("Stats Regions") + " | Betcon v" + mainWindows.version)
        try:
            self.initData()
        except Exception:
            print(_("Error trying to load the data."))
            self.setEnabled(False)

        self.cmbYear.activated.connect(self.updateMonths)
        self.cmbMonth.activated.connect(self.updateTree)

    def initData(self):
        self.years, self.months = LibStats.getYears()
        self.cmbYear.addItems(self.years.keys())

        firstKey = next(iter(self.years))
        self.cmbMonth.addItems(self.getMonths(firstKey))

        data = LibStats.getRegion()

        items = []
        for i in data:
            item = QTreeWidgetItem(i)
            item = paint_row(item, i[5])
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

        data = LibStats.getRegion(year, month)
        self.treeMonth.clear()

        items = []
        for i in data:
            item = QTreeWidgetItem(i)
            item = paint_row(item, i[5])
            items.append(item)
        self.treeMonth.addTopLevelItems(items)

    def getMonths(self, year):
        sMonths = []
        for i in self.years[year]:
            sMonths.append(self.months[i])
        return sMonths
