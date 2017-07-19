import sys
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5 import uic

from banks import Banks

class NewBank(QWidget):
    def __init__(self, mainWindows):
        QWidget.__init__(self)
        uic.loadUi("../ui/new_bank.ui", self)
        self.mainWindows = mainWindows
        self.mainWindows.setWindowTitle("Nuevo Movimiento del Bank | Betcon")

    def close(self):
            self.mainWindows.setCentralWidget(Banks(self.mainWindows))

    def cancel(self):
        self.close()

    def accept(self):
        err = 0

        if err == 0:
            QMessageBox.information(self, "Añadido", "Nuevo movimiento añadido.")
        else:
            QMessageBox.critical(self, "Error", str(err))

        self.close()

