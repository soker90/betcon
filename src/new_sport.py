import sys
import os
from lib.paths import get_base_dir
import inspect
from PySide6.QtWidgets import QMessageBox, QWidget
from uiloader import loadUi
directory = get_base_dir()
sys.path.append(directory + "/lib")
from bbdd import Bbdd
from sports import Sports

class NewSport(QWidget):
    def __init__(self, mainWindows):
        QWidget.__init__(self)
        loadUi(directory + "/../ui/new_sport.ui", self)
        self.mainWindows = mainWindows
        self.btnAccept.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.cancel)
        self.mainWindows.setWindowTitle(_("New Sport") + " | Betcon v" + mainWindows.version)
        self.txtName.returnPressed.connect(self.btnAccept.click)
        self.translate()
        self.lblImage.hide()
        self.btnBrowse.hide()
        self.lblBrowse.hide()

    def translate(self):

        self.lblName.setText(_("Name"))

        self.btnCancel.setText(_("Cancel"))
        self.btnAccept.setText(_("Accept"))

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

        QMessageBox.information(self, _("Added"), _("New sport added."))

        self.close()

