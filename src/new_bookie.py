import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget, QFileDialog
from PyQt5 import uic
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")



from bookies import Bookies
from bookie import Bookie
from gettext import gettext as _
import gettext

class NewBookie(QWidget):
    def __init__(self, mainWindows):
        QWidget.__init__(self)
        uic.loadUi(directory + "/../ui/new_bookie.ui", self)
        gettext.textdomain("betcon")
        gettext.bindtextdomain("betcon", "../lang/mo")
        self.mainWindows = mainWindows
        self.btnAccept.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.cancel)
        self.mainWindows.setWindowTitle(_("New Bookie") + " | Betcon v" + mainWindows.version)
        self.txtName.returnPressed.connect(self.btnAccept.click)
        self.translate()

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

