import sys
from PyQt5.QtWidgets import QMessageBox, QWidget, QTreeWidgetItem
from PyQt5 import uic


class StatsRegion(QWidget):
    def __init__(self, mainWindows):
        QWidget.__init__(self)
        uic.loadUi("../ui/stats_region.ui", self)
        self.mainWindows = mainWindows
        self.mainWindows.setWindowTitle("Estadisticas Regiones | Betcon")
