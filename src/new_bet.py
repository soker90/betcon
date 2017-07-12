import sys
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QWidget, QGridLayout, QAction, QPushButton, QShortcut
from PyQt5 import uic
from PyQt5.QtCore import QDateTime, QVariant
from bets import Bets
sys.path.append("./lib")
from bbdd import Bbdd

class NewBet(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		uic.loadUi("../ui/new_bet.ui", self)
		self.mainWindows = mainWindows
		self.mainWindows.setWindowTitle("Nueva Apuesta | Betcon")
		self.btnAccept.clicked.connect(self.accept)
		self.btnCancel.clicked.connect(self.cancel)
		self.initData()
		self.cmbRegion.activated.connect(self.setCompetition)
		self.cmbSport.activated.connect(self.setCompetition)

		#self.txtQuota.activated.connect(self.setCompetition)



	def initData(self):
		#dtDate
		curent_t = QDateTime().currentDateTime()
		self.dtDate.setDateTime(curent_t)

		#cmbSport
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

		# cmbRegion
		data = bd.select("region", "name")

		self.regionIndexToId = {}
		index = 0
		for i in data:
			id = i[0]
			name = i[1]
			self.cmbRegion.addItem(name)
			self.regionIndexToId[index] = id
			index += 1

		#cmbBookie
		data = bd.select("bookie", "name")

		self.bookieIndexToId = {}
		index = 0
		for i in data:
			id = i[0]
			name = i[1]
			self.cmbBookie.addItem(name)
			self.bookieIndexToId[index] = id
			index += 1

		# cmbMarket
		data = bd.select("market", "name")

		self.marketIndexToId = {}
		index = 0
		for i in data:
			id = i[0]
			name = i[1]
			self.cmbMarket.addItem(name)
			self.marketIndexToId[index] = id
			index += 1

		bd.close()

		#cmbCompetition
		self.setCompetition()

	def setCompetition(self):
		self.cmbCompetition.clear()
		bd = Bbdd()

		idRegion = self.regionIndexToId.get(self.cmbRegion.currentIndex())
		idSport = self.sportIndexToId.get(self.cmbSport.currentIndex())

		where = "region=" + str(idRegion) + " AND sport=" + str(idSport)

		data = bd.select("competition", "name", where)

		self.competitionIndexToId = {}
		index = 0
		for i in data:
			id = i[0]
			name = i[1]
			self.cmbCompetition.addItem(name)
			self.competitionIndexToId[index] = id
			index += 1

		bd.close()



	def close(self):
			self.mainWindows.setCentralWidget(Bets(self.mainWindows))

	def cancel(self):
		self.close()

	def accept(self):
		data = []

		bbdd = Bbdd()

		#dtDate
		data.append(self.dtDate.dateTime().toPyDateTime())

		#cmbSport
		idSport = self.sportIndexToId.get(self.cmbSport.currentIndex())
		data.append(idSport)

		# cmbCompetition
		idCompetition = self.competitionIndexToId.get(self.cmbCompetition.currentIndex())
		data.append(idCompetition)

		#cmbRegion
		idRegion = self.regionIndexToId.get(self.cmbRegion.currentIndex())
		data.append(idRegion)

		data.append(self.txtPlayer1.text())
		data.append(self.txtPlayer2.text())
		data.append(self.txtPick.text())

		#cmbBookie
		idBookie = self.bookieIndexToId.get(self.cmbBookie.currentIndex())
		data.append(idBookie)

		#cmbMarket
		idMarket = self.marketIndexToId.get(self.cmbMarket.currentIndex())
		data.append(idMarket)

		data.append("")
		data.append(self.txtStake.text())
		data.append(self.txtOne.text())
		data.append("")
		data.append("")
		data.append(self.txtBet.text())
		data.append(self.txtQuota.text())


		columns = ["date", "sport", "competition", "region", "player1", "player2", "pick", "bookie", "market",
				   "tipster", "stake", "one", "result", "profit", "bet", "quota"]


		bbdd.insert(columns, data, "bet")
		bbdd.close()


		QMessageBox.information(self, "Añadida", "Nueva apuesta añadida.")
		self.close()

