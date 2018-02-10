import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5 import uic
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from bbdd import Bbdd
from sports import Sports
from gettext import gettext as _
import gettext

class NewSport(QWidget):
    def __init__(self, mainWindows):
        QWidget.__init__(self)
        uic.loadUi(directory + "/../ui/new_sport.ui", self)
        gettext.textdomain("betcon")
        gettext.bindtextdomain("betcon", "../lang/mo")
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

