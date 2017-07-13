import sys
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5 import uic
sys.path.append("./lib")
from bbdd import Bbdd
from bookies import Bookies

class EditBookie(QWidget):
    def __init__(self, mainWindows, id):
        QWidget.__init__(self)
        uic.loadUi("../ui/new_bookie.ui", self)
        self.mainWindows = mainWindows
        self.btnAccept.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.cancel)
        self.mainWindows.setWindowTitle("Modificar Casa | Betcon")
        self.txtName.returnPressed.connect(self.btnAccept.click)

        self.id = id
        self.initData()

    def initData(self):
        bd = Bbdd()

        name = bd.getValue(self.id, "bookie")
        self.txtName.setText(name)

    def close(self):
            self.mainWindows.setCentralWidget(Bookies(self.mainWindows))

    def cancel(self):
        self.close()

    def accept(self):
        data = [self.txtName.text()]
        columns = ["name"]

        bbdd = Bbdd()
        bbdd.update(columns, data, "bookie", self.id)
        bbdd.close()

        QMessageBox.information(self, "Actualizada", "Casa actualizada.")

        self.close()

