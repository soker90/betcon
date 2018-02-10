import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget, QFileDialog
from PyQt5 import uic

from new_sport import NewSport
from os.path import expanduser

directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from bbdd import Bbdd
from sports import Sports
from gettext import gettext as _
import gettext
from shutil import copy2
from images import Images

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
		self.ruta = None
		self.initData()
		NewSport.translate(self)
		self.btnBrowse.clicked.connect(self.browseImage)

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

		if self.ruta is not None:
			try:
				if not os.path.exists(expanduser("~") + "/.betcon/resources/sports"):
					os.makedirs(expanduser("~") + "/.betcon/resources/sports")
				copy2(self.ruta, expanduser("~") + "/.betcon/resources/sports/" + self.id + ".png")
				img = Images(expanduser("~") + "/.betcon/resources/sports/" + self.id + ".png")
				img.resize(100, 20)
			except:
				msg = "Imágen incorrecta"

		QMessageBox.information(self, _("Updated"), _("Updated sport."))

		self.close()

	def browseImage(self):
		file = QFileDialog.getOpenFileName(None, _("Image of the bookie"), expanduser("~/"), "*.png")
		if file[0] != '':
			self.ruta = file[0]
			self.lblBrowse.setText(self.ruta)

