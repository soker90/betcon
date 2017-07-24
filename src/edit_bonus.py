import sys
from PyQt5.QtWidgets import QMessageBox, QWidget, QComboBox
from PyQt5 import uic
sys.path.append("./lib")
from bbdd import Bbdd
from bonus import Bonus
from func_aux import str_to_float

class EditBonus(QWidget):
	def __init__(self, mainWindows, id):
		QWidget.__init__(self)
		uic.loadUi("../ui/new_bonus.ui", self)
		self.mainWindows = mainWindows
		self.btnAccept.clicked.connect(self.accept)
		self.btnCancel.clicked.connect(self.cancel)
		self.mainWindows.setWindowTitle("Modificar Bonus | Betcon")
		self.initData()
		self.id = id
		self.initData()

	def initData(self):
		bd = Bbdd()

		where = str(self.id)
		# date
		#dataBonus = bd.select("bonus", None, where)
		#date = QDate.fromString(dataBonus[1], "yyyy-MM-dd")
		#self.txtDate.setDate(date)

		# cmbBookie
		data = bd.select("bookie", "name")

		self.bookieIndexToId = {}
		index = 0
		for i in data:
			id = i[0]
			name = i[1]
			self.cmbBookie.addItem(name)
			self.bookieIndexToId[index] = id
			index += 1

		bd.close()

	def close(self):
			self.mainWindows.setCentralWidget(Bonus(self.mainWindows))

	def cancel(self):
		self.close()

	def accept(self):
		data = []

		bbdd = Bbdd()

		# dtDate
		data.append(self.txtDate.dateTime().toPyDateTime())

		# cmbBookie
		idBookie = self.bookieIndexToId.get(self.cmbBookie.currentIndex())
		data.append(idBookie)

		data.append(str(str_to_float(self.txtMoney.text())))
		data.append(self.chkFree.isChecked())

		columns = ["date", "bookie", "money", "free"]

		bbdd.update(columns, data, "bonus", self.id)

		QMessageBox.information(self, "Actualizado", "Bono actualizado.")

		self.close()

