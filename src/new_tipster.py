import sys
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5 import uic
sys.path.append("./lib")
from bbdd import Bbdd
from tipsters import Tipsters

class NewTipster(QWidget):
    def __init__(self, mainWindows):
        QWidget.__init__(self)
        uic.loadUi("../ui/new_tipster.ui", self)
        self.mainWindows = mainWindows
        self.btnAccept.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.cancel)
        self.mainWindows.setWindowTitle("Nuevo Tipster | Betcon v" + mainWindows.version)
        self.txtName.returnPressed.connect(self.btnAccept.click)

    def close(self):
            self.mainWindows.setCentralWidget(Tipsters(self.mainWindows))
            #self.mainWindows.aApuesta.setEnabled(True)

    def cancel(self):
        self.close()

    def accept(self):
        data = [self.txtName.text()]
        columns = ["name"]

        bbdd = Bbdd()
        bbdd.insert(columns, data, "tipster")
        bbdd.close()

        QMessageBox.information(self, "Añadido", "Nuevo tipster añadido.")

        self.close()

