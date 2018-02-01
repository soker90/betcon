import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5 import uic

from new_region import NewRegion

directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from bbdd import Bbdd
from regions import Regions
from gettext import gettext as _
import gettext

class EditRegion(QWidget):
	def __init__(self, mainWindows, id):
		QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/new_region.ui", self)
		gettext.textdomain("betcon")
		gettext.bindtextdomain("betcon", "../lang/mo")
		self.mainWindows = mainWindows
		self.btnAccept.clicked.connect(self.accept)
		self.btnCancel.clicked.connect(self.cancel)
		self.mainWindows.setWindowTitle(_("New Region") + " | Betcon v" + mainWindows.version)
		self.txtRegion.returnPressed.connect(self.btnAccept.click)

		self.id = id
		self.initData()
		NewRegion.translate(self)

	def initData(self):
		bd = Bbdd()

		name = bd.getValue(self.id, "region")
		self.txtRegion.setText(name)

		bd.close()

	def close(self):
			self.mainWindows.setCentralWidget(Regions(self.mainWindows))

	def cancel(self):
		self.close()

	def accept(self):
		data = [self.txtRegion.text()]
		columns = ["name"]

		bbdd = Bbdd()
		bbdd.update(columns, data, "region", "id="+self.id)
		bbdd.close()

		QMessageBox.information(self, _("Updated"), _("Updated region."))

		self.close()

