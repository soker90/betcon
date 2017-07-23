import sys
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5 import uic
sys.path.append("./lib")
from bbdd import Bbdd
from banks import Banks
from func_aux import str_to_float
from datetime import datetime
from PyQt5.QtCore import QDate

class NewBank(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		uic.loadUi("../ui/new_bank.ui", self)
		self.mainWindows = mainWindows
		self.btnAccept.clicked.connect(self.accept)
		self.btnCancel.clicked.connect(self.cancel)
		self.mainWindows.setWindowTitle("Nuevo Movimiento | Betcon")
		self.initData()

	def initData(self):
		sDate = datetime.now().strftime('%Y-%m-%d')
		dDate = QDate.fromString(sDate, "yyyy-MM-dd")
		self.txtDate.setDate(dDate)

		# cmbBookie
		bd = Bbdd()
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
		self.mainWindows.setCentralWidget(Banks(self.mainWindows))

	def cancel(self):
		self.close()

	def accept(self):
		data = []

		data.append(self.txtDate.text())
		data.append(self.cmbAccount.currentIndex()+1)
		idBookie = self.bookieIndexToId.get(self.cmbBookie.currentIndex())
		data.append(idBookie)
		if self.cmbType.currentIndex() == 1:
			type = "-"
		else:
			type = ""

		money = type+str(self.txtMoney.text())
		money = str_to_float(money)
		data.append(money)

		columns = ["date", "account", "bookie", "money"]

		bbdd = Bbdd()
		bbdd.insert(columns, data, "movement")

		money *= -1
		data = ["'+bank+'" + str(money)]
		columns = ["bank"]

		account = self.cmbAccount.currentIndex()
		bbdd.update(columns, data, "bank", "id="+str(account + 1))
		bbdd.close()

		QMessageBox.information(self, "Añadido", "Movimiento añadido.")
		self.close()

