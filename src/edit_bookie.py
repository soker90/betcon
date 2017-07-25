import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5 import uic
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from bookies import Bookies
from bookie import Bookie

class EditBookie(QWidget):
    def __init__(self, mainWindows, id):
        QWidget.__init__(self)
        uic.loadUi(directory + "/../ui/new_bookie.ui", self)
        self.mainWindows = mainWindows
        self.btnAccept.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.cancel)
        self.mainWindows.setWindowTitle("Modificar Casa | Betcon v" + mainWindows.version)
        self.txtName.returnPressed.connect(self.btnAccept.click)

        self.item = Bookie()
        self.item.setId(id)

        self.initData()

    def initData(self):
        self.txtName.setText(self.item.name)

    def close(self):
            self.mainWindows.setCentralWidget(Bookies(self.mainWindows))

    def cancel(self):
        self.close()

    def accept(self):
        self.item.setName(self.txtName.text())
        err = self.item.update()

        if err == 0:
            QMessageBox.information(self, "Actualizada", "Casa actualizada.")
        else:
            QMessageBox.critical(self, "Error", str(err))

        self.close()

