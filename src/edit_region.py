import sys
import os
from lib.paths import get_base_dir
import inspect
from PySide6.QtWidgets import QMessageBox, QWidget
from uiloader import loadUi

from new_region import NewRegion

directory = get_base_dir()
sys.path.append(directory + "/lib")
from bbdd import Bbdd
from regions import Regions

class EditRegion(QWidget):
	def __init__(self, mainWindows, id):
		QWidget.__init__(self)
		loadUi(directory + "/../ui/new_region.ui", self)
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
		bbdd.update(columns, data, "region", "id=?", (self.id,))
		bbdd.close()

		QMessageBox.information(self, _("Updated"), _("Updated region."))

		self.close()

