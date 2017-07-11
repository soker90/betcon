import sys
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5 import uic
sys.path.append("./lib")
from bbdd import Bbdd
from bookies import Bookies

class NewBookie(QWidget):
    def __init__(self, mainWindows):
        QWidget.__init__(self)
        uic.loadUi("../ui/new_bookie.ui", self)
        self.mainWindows = mainWindows
        self.btnAccept.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.cancel)
        self.mainWindows.setWindowTitle("Nueva Casa | Betcon")
        self.txtName.returnPressed.connect(self.btnAccept.click)

    def close(self):
            self.mainWindows.setCentralWidget(Bookies(self.mainWindows))
            #self.mainWindows.aApuesta.setEnabled(True)

    def cancel(self):
        self.close()

    def accept(self):
        data = [self.txtName.text()]
        columns = ["name"]

        bbdd = Bbdd()
        bbdd.insert(columns, data, "bookie")
        bbdd.close()

        QMessageBox.information(self, "Añadida", "Nueva casa añadida.")

        self.close()

