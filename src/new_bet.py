import sys, os, inspect
from datetime import datetime
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QWidget, QComboBox, QAction, QPushButton, QShortcut
from PyQt5 import uic
from PyQt5.QtCore import QDateTime, QVariant
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from bets import Bets
from decimal import Decimal
from func_aux import str_to_float, str_to_bool

from bbdd import Bbdd


class NewBet(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/new_bet.ui", self)
		self.mainWindows = mainWindows
		self.mainWindows.setWindowTitle("Nueva Apuesta | Betcon v" + mainWindows.version)
		self.btnAccept.clicked.connect(self.accept)
		self.btnCancel.clicked.connect(self.cancel)
		self.initData()
		self.cmbRegion.activated.connect(self.setCompetition)
		self.cmbSport.activated.connect(self.setRegion)
		self.cmbResult.activated.connect(self.updateProfit)
		self.txtQuota.valueChanged.connect(self.updateProfit)
		self.txtBet.valueChanged.connect(self.updateProfit)
		self.chkFree.clicked.connect(self.freeBet)
		self.txtStake.valueChanged.connect(self.updateBet)
		self.txtOne.valueChanged.connect(self.updateBet)

	# self.txtQuota.activated.connect(self.setCompetition)



	def initData(self):
		# dtDate
		sDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		date = QDateTime.fromString(sDate, "yyyy-MM-dd hh:mm:ss")
		self.dtDate.setDateTime(date)

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

		# cmbTipster
		data = bd.select("tipster", "name")

		self.tipsterIndexToId = {}
		index = 0
		for i in data:
			id = i[0]
			name = i[1]
			self.cmbTipster.addItem(name)
			self.tipsterIndexToId[index] = id
			index += 1

		bd.close()

		# cmbCompetition
		self.setRegion()

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

		if index == 0:
			self.btnAccept.setDisabled(True)
		else:
			self.btnAccept.setDisabled(False)

		bd.close()

	def setRegion(self):
		self.btnAccept.setDisabled(False)
		self.cmbRegion.clear()
		bd = Bbdd()

		idSport = self.sportIndexToId.get(self.cmbSport.currentIndex())

		where = " sport=" + str(idSport)

		data = bd.select("competition", None, where, "region")
		dataRegion = ""

		if len(data) > 0:
			sData = "("
			j= 0
			for i in data:
				if j == len(data)-1:
					sData += str(i[0]) + ")"
				else:
					sData += str(i[0]) + ", "
				j+=1

			where = " id in "+sData
			dataRegion = bd.select("region", "name", where)

			if len(dataRegion) < 1:
				self.btnAccept.setDisabled(True)
				bd.close()
			else:
				self.regionIndexToId = {}
				index = 0
				for i in dataRegion:
					id = i[0]
					name = i[1]
					self.cmbRegion.addItem(name)
					self.regionIndexToId[index] = id
					index += 1
				bd.close()
				self.setCompetition()

		else:
			self.btnAccept.setDisabled(True)
			bd.close()

		if len(data) == 0 or len(dataRegion):
			self.btnAccept.setDisabled(True)
		else:
			self.btnAccept.setDisabled(False)

	def close(self):
		self.mainWindows.setCentralWidget(Bets(self.mainWindows))

	def cancel(self):
		self.close()

	def accept(self):
		data = []

		bbdd = Bbdd()

		# dtDate
		data.append(self.dtDate.dateTime().toPyDateTime())

		# cmbSport
		idSport = self.sportIndexToId.get(self.cmbSport.currentIndex())
		data.append(idSport)

		# cmbCompetition
		idCompetition = self.competitionIndexToId.get(self.cmbCompetition.currentIndex())
		data.append(idCompetition)

		# cmbRegion
		idRegion = self.regionIndexToId.get(self.cmbRegion.currentIndex())
		data.append(idRegion)

		data.append(self.txtPlayer1.text())
		data.append(self.txtPlayer2.text())
		data.append(self.txtPick.text())

		# cmbBookie
		idBookie = self.bookieIndexToId.get(self.cmbBookie.currentIndex())
		data.append(idBookie)

		# cmbMarket
		idMarket = self.marketIndexToId.get(self.cmbMarket.currentIndex())
		data.append(idMarket)

		# cmbTipster
		idTipster = self.tipsterIndexToId.get(self.cmbTipster.currentIndex())
		data.append(idTipster)

		data.append(str(str_to_float(self.txtStake.text())))
		data.append(str(str_to_float(self.txtOne.text())))

		# cmbResult
		data.append(self.cmbResult.currentText())

		data.append(str(str_to_float(self.txtProfit.text())))
		data.append(str(str_to_float(self.txtBet.text())))
		data.append(str(str_to_float(self.txtQuota.text())))
		data.append(1 if self.chkFree.isChecked() else 0)

		columns = ["date", "sport", "competition", "region", "player1", "player2", "pick", "bookie", "market",
		           "tipster", "stake", "one", "result", "profit", "bet", "quota", "free"]

		bbdd.insert(columns, data, "bet")
		bbdd.close()

		QMessageBox.information(self, "Añadida", "Nueva apuesta añadida.")
		self.close()

	def updateProfit(self):
		result = self.cmbResult.currentIndex()
		quota = self.txtQuota.value()
		bet = self.txtBet.value()

		if self.chkFree.isChecked():
			profit = {
				0: lambda quota: 0,  # Pendiente
				1: lambda quota: quota - 1,  # Acertada
				2: lambda quota: 0,  # Fallada
				3: lambda quota: 0,  # Nula
				4: lambda quota: (quota - 1) * 0.5,  # Medio Acertada
				5: lambda quota: 0,  # Medio Fallada
				6: lambda quota: 0  # Retirada
			}[result](float(quota))
		else:
			profit = {
				0: lambda quota: -1,  # Pendiente
				1: lambda quota: quota - 1,  # Acertada
				2: lambda quota: -1,  # Fallada
				3: lambda quota: 0,  # Nula
				4: lambda quota: (quota - 1) * 0.5,  # Medio Acertada
				5: lambda quota: (quota - 1) * -0.5,  # Medio Fallada
				6: lambda quota: 0  # Retirada
			}[result](float(quota))

		profit *= bet

		self.txtProfit.setValue(profit)

	def freeBet(self):
		self.updateProfit()

	def updateBet(self):
		if self.txtStake.text() != "0,00" and self.txtOne.text() != "0,00":
			bet = str_to_float(self.txtStake.text()) * str_to_float(self.txtOne.text())
			self.txtBet.setValue(bet)

