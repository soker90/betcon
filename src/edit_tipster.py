import sys
import os
from lib.paths import get_base_dir
import inspect

from new_tipster import NewTipster

directory = get_base_dir()
sys.path.append(directory + "/lib")
from PySide6.QtWidgets import QMessageBox, QWidget
from uiloader import loadUi
from bbdd import Bbdd
from tipsters import Tipsters

class EditTipster(QWidget):
    def __init__(self, mainWindows, id):
        QWidget.__init__(self)
        loadUi(directory + "/../ui/new_tipster.ui", self)
        self.mainWindows = mainWindows
        self.btnAccept.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.cancel)
        self.mainWindows.setWindowTitle(_("Modify Tipster") + " | Betcon v" + mainWindows.version)
        self.txtName.returnPressed.connect(self.btnAccept.click)

        self.id = id
        self.initData()
        NewTipster.translate(self)

    def initData(self):
        bd = Bbdd()

        name = bd.getValue(self.id, "tipster")
        self.txtName.setText(name)

        bd.close()

    def close(self):
            self.mainWindows.setCentralWidget(Tipsters(self.mainWindows))

    def cancel(self):
        self.close()

    def accept(self):
        data = [self.txtName.text()]
        columns = ["name"]

        bbdd = Bbdd()
        bbdd.update(columns, data, "tipster", "id=?", (self.id,))
        bbdd.close()

        QMessageBox.information(self, _("Updated"), _("Updated tipster."))

        self.close()

