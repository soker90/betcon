import sys
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5 import uic
sys.path.append("./lib")
from bbdd import Bbdd
from regions import Regions

class EditRegion(QWidget):
	def __init__(self, mainWindows, id):
		QWidget.__init__(self)
		uic.loadUi("../ui/new_region.ui", self)
		self.mainWindows = mainWindows
		self.btnAccept.clicked.connect(self.accept)
		self.btnCancel.clicked.connect(self.cancel)
		self.mainWindows.setWindowTitle("Nueva Región | Betcon")
		self.txtRegion.returnPressed.connect(self.btnAccept.click)

		self.id = id
		self.initData()

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
		bbdd.update(columns, data, "region", self.id)
		bbdd.close()

		QMessageBox.information(self, "Actualizada", "Región actualizada.")

		self.close()

