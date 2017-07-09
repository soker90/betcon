import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic


class Principal(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi("../qt/principal.ui", self)


