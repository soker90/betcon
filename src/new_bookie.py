import sys
import os
import inspect
from PySide6.QtWidgets import QMessageBox, QWidget
from uiloader import loadUi
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")



from bookies import Bookies
from bookie import Bookie

class NewBookie(QWidget):
    def __init__(self, mainWindows):
        QWidget.__init__(self)
        loadUi(directory + "/../ui/new_bookie.ui", self)
        self.mainWindows = mainWindows
        self.btnAccept.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.cancel)
        self.mainWindows.setWindowTitle(_("New Bookie") + " | Betcon v" + mainWindows.version)
        self.txtName.returnPressed.connect(self.btnAccept.click)
        self.translate()
        self.lblImage.hide()
        self.btnBrowse.hide()
        self.lblBrowse.hide()

    def translate(self):

        self.lblName.setText(_("Name"))
        self.lblCountry.setText(_("Country"))
        self.btnBrowse.setText(_("Browse..."))

        self.btnCancel.setText(_("Cancel"))
        self.btnAccept.setText(_("Accept"))

    def close(self):
            self.mainWindows.setCentralWidget(Bookies(self.mainWindows))

    def cancel(self):
        self.close()

    def accept(self):

        bookie = Bookie()
        bookie.setAll(self.txtName.text(), self.txtCountry.text())
        err = bookie.insert()

        if err == 0:
            QMessageBox.information(self, _("Added"), _("New bookie added."))
        else:
            QMessageBox.critical(self, _("Error"), str(err))

        self.close()

