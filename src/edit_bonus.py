import sys
from PyQt5.QtWidgets import QMessageBox, QWidget, QComboBox
from PyQt5 import uic
from PyQt5.QtCore import QDate
sys.path.append("./lib")
from bbdd import Bbdd
from bonus import Bonus
from func_aux import str_to_float, str_to_bool

class EditBonus(QWidget):
	def __init__(self, mainWindows, id):
		QWidget.__init__(self)
		uic.loadUi("../ui/new_bonus.ui", self)
		self.mainWindows = mainWindows
		self.btnAccept.clicked.connect(self.accept)
		self.btnCancel.clicked.connect(self.cancel)
		self.mainWindows.setWindowTitle("Modificar Bonus | Betcon")

		self.id = id
		self.initData()

	def initData(self):
		bd = Bbdd()

		where = "id=" + str(self.id)
		# date
		dataBonus = bd.select("bonus", None, where)[0]
		date = QDate.fromString(dataBonus[1], "yyyy-MM-dd")
		self.txtDate.setDate(date)

		# cmbBookie
		data = bd.select("bookie", "name")

		self.bookieIndexToId = {}
		index, idCmb = 0, 0
		for i in data:
			id = i[0]
			if dataBonus[2] == id:
				idCmb = index
			name = i[1]
			self.cmbBookie.addItem(name)
			self.bookieIndexToId[index] = id
			index += 1

		self.cmbBookie.setCurrentIndex(idCmb)

		self.txtMoney.setValue(dataBonus[3])

		self.chkFree.setChecked(str_to_bool(dataBonus[4]))

		bd.close()

	def close(self):
			self.mainWindows.setCentralWidget(Bonus(self.mainWindows))

	def cancel(self):
		self.close()

	def accept(self):
		data = []

		bbdd = Bbdd()

		# dtDate
		data.append(self.txtDate.date().toPyDate())

		# cmbBookie
		idBookie = self.bookieIndexToId.get(self.cmbBookie.currentIndex())
		data.append(idBookie)

		data.append(str(str_to_float(self.txtMoney.text())))

		free = self.chkFree.isChecked()
		data.append(free)

		columns = ["date", "bookie", "money", "free"]

		bbdd.update(columns, data, "bonus", "id="+self.id)

		QMessageBox.information(self, "Actualizado", "Bono actualizado.")

		self.close()

