import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic


class Bets(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi("../ui/bets.ui", self)


