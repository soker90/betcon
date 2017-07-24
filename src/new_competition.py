import sys
from PyQt5.QtWidgets import QMessageBox, QWidget, QComboBox
from PyQt5 import uic
sys.path.append("./lib")
from bbdd import Bbdd
from competitions import Competitions

class NewCompetition(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		uic.loadUi("../ui/new_competition.ui", self)
		self.mainWindows = mainWindows
		self.btnAccept.clicked.connect(self.accept)
		self.btnCancel.clicked.connect(self.cancel)
		self.mainWindows.setWindowTitle("Nueva Competición | Betcon v" + mainWindows.version)
		self.txtName.returnPressed.connect(self.btnAccept.click)
		self.initData()

	def initData(self):
		# cmbRegion
		bd = Bbdd()
		data = bd.select("region", "name")

		self.regionIndexToId = {}
		index = 0
		for i in data:
			id = i[0]
			name = i[1]
			self.cmbRegion.addItem(name)
			self.regionIndexToId[index] = id
			index += 1

		# cmbSport
		bd = Bbdd()
		data = bd.select("sport", "name")

		self.sportIndexToId = {}
		index = 0
		for i in data:
			id = i[0]
			name = i[1]
			self.cmbSport.addItem(name)
			self.sportIndexToId[index] = id
			index += 1

		bd.close()

	def close(self):
			self.mainWindows.setCentralWidget(Competitions(self.mainWindows))

	def cancel(self):
		self.close()

	def accept(self):
		data = []
		data.append(self.txtName.text())
		idRegion = self.regionIndexToId.get(self.cmbRegion.currentIndex())
		data.append(idRegion)
		idSport = self.sportIndexToId.get(self.cmbSport.currentIndex())
		data.append(idSport)



		columns = ["name", "region", "sport"]

		bbdd = Bbdd()
		bbdd.insert(columns, data, "competition")
		bbdd.close()

		QMessageBox.information(self, "Añadida", "Nueva competición añadida.")

		self.close()

