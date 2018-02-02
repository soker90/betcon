import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5 import uic

from new_sport import NewSport

directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from bbdd import Bbdd
from sports import Sports
from gettext import gettext as _
import gettext

class EditSport(QWidget):
	def __init__(self, mainWindows, id):
		QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/new_sport.ui", self)
		gettext.textdomain("betcon")
		gettext.bindtextdomain("betcon", "../lang/mo")
		self.mainWindows = mainWindows
		self.btnAccept.clicked.connect(self.accept)
		self.btnCancel.clicked.connect(self.cancel)
		self.mainWindows.setWindowTitle(_("New Sport") + " | Betcon v" + mainWindows.version)
		self.txtName.returnPressed.connect(self.btnAccept.click)

		self.id = id
		self.initData()
		NewSport.translate(self)

	def initData(self):
		bd = Bbdd()

		name = bd.getValue(self.id, "sport")
		self.txtName.setText(name)

		bd.close()

	def close(self):
			self.mainWindows.setCentralWidget(Sports(self.mainWindows))

	def cancel(self):
		self.close()

	def accept(self):
		data = [self.txtName.text()]
		columns = ["name"]

		bbdd = Bbdd()
		bbdd.update(columns, data, "sport", "id="+self.id)
		bbdd.close()

		QMessageBox.information(self, _("Updated"), _("Updated sport."))

		self.close()

