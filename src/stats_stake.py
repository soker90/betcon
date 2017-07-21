import sys
from PyQt5.QtWidgets import QMessageBox, QWidget, QTreeWidgetItem
from PyQt5 import uic


class StatsStake(QWidget):
    def __init__(self, mainWindows):
        QWidget.__init__(self)
        uic.loadUi("../ui/stats_stake.ui", self)
        self.mainWindows = mainWindows
        self.mainWindows.setWindowTitle("Estadisticas Stake | Betcon")
