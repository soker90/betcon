import sys
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5 import uic
sys.path.append("./lib")
from bbdd import Bbdd
from sports import Sports

class NewSport(QWidget):
    def __init__(self, mainWindows):
        QWidget.__init__(self)
        uic.loadUi("../ui/new_sport.ui", self)
        self.mainWindows = mainWindows
        self.btnAccept.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.cancel)
        self.mainWindows.setWindowTitle("Nuevo Deporte | Betcon v" + mainWindows.version)
        self.txtName.returnPressed.connect(self.btnAccept.click)

    def close(self):
            self.mainWindows.setCentralWidget(Sports(self.mainWindows))
            #self.mainWindows.aApuesta.setEnabled(True)

    def cancel(self):
        self.close()

    def accept(self):
        data = [self.txtName.text()]
        columns = ["name"]

        bbdd = Bbdd()
        bbdd.insert(columns, data, "sport")
        bbdd.close()

        QMessageBox.information(self, "Añadido", "Nuevo deporte añadido.")

        self.close()

