import sys, os, inspect
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5 import uic
from bbdd import Bbdd
from tipsters import Tipsters
from gettext import gettext as _
import gettext

class EditTipster(QWidget):
    def __init__(self, mainWindows, id):
        QWidget.__init__(self)
        uic.loadUi(directory + "/../ui/new_tipster.ui", self)
        gettext.textdomain("betcon")
        gettext.bindtextdomain("betcon", "../lang/mo")
        self.mainWindows = mainWindows
        self.btnAccept.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.cancel)
        self.mainWindows.setWindowTitle(_("Modify Tipster") + " | Betcon v" + mainWindows.version)
        self.txtName.returnPressed.connect(self.btnAccept.click)

        self.id = id
        self.initData()

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
        bbdd.update(columns, data, "tipster", "id="+self.id)
        bbdd.close()

        QMessageBox.information(self, _("Updated"), _("Updated tipster."))

        self.close()

