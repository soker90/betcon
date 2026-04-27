import sys
import os
from lib.paths import get_base_dir
import inspect
from PySide6.QtWidgets import QMessageBox, QWidget, QFileDialog
from uiloader import loadUi

from new_bookie import NewBookie

directory = get_base_dir()
sys.path.append(directory + "/lib")
from bookies import Bookies
from bookie import Bookie
from os.path import expanduser

class EditBookie(QWidget):
    def __init__(self, mainWindows, id):
        QWidget.__init__(self)
        loadUi(directory + "/../ui/new_bookie.ui", self)
        self.mainWindows = mainWindows
        self.btnAccept.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.cancel)
        self.mainWindows.setWindowTitle(_("Modify Bookie") + " | Betcon v" + mainWindows.version)
        self.txtName.returnPressed.connect(self.btnAccept.click)

        self.item = Bookie()
        self.item.setId(id)
        self.btnBrowse.clicked.connect(self.browseImage)

        self.initData()
        NewBookie.translate(self)

    def initData(self):
        self.txtName.setText(self.item.name)
        self.txtCountry.setText(self.item.country)

    def browseImage(self):
            file = QFileDialog.getOpenFileName(None, _("Image of the bookie"), expanduser("~/"), "*.png")
            if file[0] != '':
                ruta = file[0]
                self.item.setRuta(ruta)
                self.lblBrowse.setText(ruta)

    def close(self):
            self.mainWindows.setCentralWidget(Bookies(self.mainWindows))

    def cancel(self):
        self.close()

    def accept(self):
        self.item.setName(self.txtName.text())
        self.item.setCountry(self.txtCountry.text())
        err = self.item.update()

        if err == 0:
            QMessageBox.information(self, _("Updated"), _("Updated bookie."))
        else:
            QMessageBox.critical(self, _("Error"), str(err))

        self.close()

