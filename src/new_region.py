import sys
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5 import uic
sys.path.append("./lib")
from bbdd import Bbdd
from regions import Regions

class NewRegion(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		uic.loadUi("../ui/new_region.ui", self)
		self.mainWindows = mainWindows
		self.btnAccept.clicked.connect(self.accept)
		self.btnCancel.clicked.connect(self.cancel)
		self.mainWindows.setWindowTitle("Nueva Región | Betcon v" + mainWindows.version)
		self.txtRegion.returnPressed.connect(self.btnAccept.click)

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

		QMessageBox.information(self, "Añadida", "Nueva región añadida.")

		self.close()

