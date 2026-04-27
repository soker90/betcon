import sys
import os
from lib.paths import get_base_dir
import inspect
from PySide6.QtWidgets import QMessageBox, QWidget
from uiloader import loadUi

from new_market import NewMarket

directory = get_base_dir()
sys.path.append(directory + "/lib")
from bbdd import Bbdd
from markets import Markets

class EditMarket(QWidget):
    def __init__(self, mainWindows, id):
        QWidget.__init__(self)
        loadUi(directory + "/../ui/new_market.ui", self)
        self.mainWindows = mainWindows
        self.btnAccept.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.cancel)
        self.mainWindows.setWindowTitle(_("Modify Market") + " | Betcon v" + mainWindows.version)
        self.txtName.returnPressed.connect(self.btnAccept.click)

        self.id = id
        self.initData()
        NewMarket.translate(self)

    def initData(self):
        bd = Bbdd()

        name = bd.getValue(self.id, "market")
        self.txtName.setText(name)

        bd.close()

    def close(self):
            self.mainWindows.setCentralWidget(Markets(self.mainWindows))

    def cancel(self):
        self.close()

    def accept(self):
        data = [self.txtName.text()]
        columns = ["name"]

        bbdd = Bbdd()
        bbdd.update(columns, data, "market", "id=?", (self.id,))
        bbdd.close()

        QMessageBox.information(self, _("Updated"), _("Market updated."))

        self.close()

