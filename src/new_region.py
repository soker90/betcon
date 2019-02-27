import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5 import uic
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from bbdd import Bbdd
from regions import Regions
from gettext import gettext as _
import gettext

class NewRegion(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/new_region.ui", self)
		gettext.textdomain("betcon")
		gettext.bindtextdomain("betcon", "../lang/mo" + mainWindows.lang)
		gettext.bindtextdomain("betcon", "/usr/share/locale" + mainWindows.lang)
		self.mainWindows = mainWindows
		self.btnAccept.clicked.connect(self.accept)
		self.btnCancel.clicked.connect(self.cancel)
		self.mainWindows.setWindowTitle(_("New Region") + " | Betcon v" + mainWindows.version)
		self.txtRegion.returnPressed.connect(self.btnAccept.click)
		self.translate()

	def translate(self):
		self.lblName.setText(_("Name"))

		self.btnCancel.setText(_("Cancel"))
		self.btnAccept.setText(_("Accept"))

	def close(self):
			self.mainWindows.setCentralWidget(Regions(self.mainWindows))
			#self.mainWindows.aApuesta.setEnabled(True)

	def cancel(self):
		self.close()

	def accept(self):
		data = [self.txtRegion.text()]
		columns = ["name"]

		bbdd = Bbdd()
		bbdd.insert(columns, data, "region")
		bbdd.close()

		QMessageBox.information(self, _("Added"), _("New region added."))

		self.close()

