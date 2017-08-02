import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5 import uic
from bets import Bets
from PyQt5.QtCore import QDateTime
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from bbdd import Bbdd
from func_aux import str_to_float, str_to_bool


class EditBet(QWidget):
	def __init__(self, mainWindows, id):
		QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/new_bet.ui", self)
		self.mainWindows = mainWindows
		self.mainWindows.setWindowTitle("Modificar Apuesta | Betcon v" + mainWindows.version)
		self.btnAccept.clicked.connect(self.accept)
		self.btnCancel.clicked.connect(self.cancel)
		self.id = id
		self.initData()
		self.cmbRegion.activated.connect(self.setCompetition)
		self.cmbSport.activated.connect(self.setCompetition)
		self.cmbResult.activated.connect(self.updateProfit)
		self.txtQuota.valueChanged.connect(self.updateProfit)
		self.txtBet.valueChanged.connect(self.updateProfit)
		self.chkFree.clicked.connect(self.freeBet)
		self.txtStake.valueChanged.connect(self.updateBet)
		self.txtOne.valueChanged.connect(self.updateBet)


	def initData(self):
		# dtDate
		bd = Bbdd()
		sDate = bd.getValue(self.id, "bet", "date")
		date = QDateTime.fromString(sDate, "yyyy-MM-dd hh:mm:ss")
		self.dtDate.setDateTime(date)

		# cmbSport

		data = bd.select("sport", "name")

		self.sportIndexToId = {}
		index, idCmb = 0, 0
		idBd = bd.getValue(self.id, "bet", "sport")
		for i in data:
			id = i[0]
			if id == idBd:
				idCmb = index
			name = i[1]
			self.cmbSport.addItem(name)
			self.sportIndexToId[index] = id
			index += 1

		self.cmbSport.setCurrentIndex(idCmb)


		# cmbBookie
		data = bd.select("bookie", "name")

		index, idCmb = 0, 0
		idBd = bd.getValue(self.id, "bet", "bookie")

		self.bookieIndexToId = {}
		index = 0
		for i in data:
			id = i[0]
			if id == idBd:
				idCmb = index
			name = i[1]
			self.cmbBookie.addItem(name)
			self.bookieIndexToId[index] = id
			index += 1

		self.cmbBookie.setCurrentIndex(idCmb)

		# txtPlayer1
		player1 = bd.getValue(self.id, "bet", "player1")
		self.txtPlayer1.setText(player1)

		# txtPlayer2
		player2 = bd.getValue(self.id, "bet", "player2")
		self.txtPlayer2.setText(player2)

		# txtPick
		pick = bd.getValue(self.id, "bet", "pick")
		self.txtPick.setText(pick)

		# cmbMarket
		data = bd.select("market", "name")

		index, idCmb = 0, -1
		idBd = bd.getValue(self.id, "bet", "market")

		self.marketIndexToId = {}
		index = 0
		for i in data:
			id = i[0]
			if id == idBd:
				idCmb = index
			name = i[1]
			self.cmbMarket.addItem(name)
			self.marketIndexToId[index] = id
			index += 1

		self.cmbMarket.setCurrentIndex(idCmb)

		# cmbTipster
		data = bd.select("tipster", "name")

		index, idCmb = 0, 0
		idBd = bd.getValue(self.id, "bet", "tipster")

		self.tipsterIndexToId = {}
		index = 0
		for i in data:
			id = i[0]
			if id == idBd:
				idCmb = index
			name = i[1]
			self.cmbTipster.addItem(name)
			self.tipsterIndexToId[index] = id
			index += 1

		self.cmbTipster.setCurrentIndex(idCmb)

		# txtStake
		stake = bd.getValue(self.id, "bet", "stake")
		self.txtStake.setValue(stake)

		# txtOne
		one = bd.getValue(self.id, "bet", "one")
		self.txtOne.setValue(one)

		# txtBet
		bet = bd.getValue(self.id, "bet", "bet")
		self.txtBet.setValue(bet)

		# txtQuota
		quota = bd.getValue(self.id, "bet", "quota")
		self.txtQuota.setValue(quota)

		# txtProfit
		profit = bd.getValue(self.id, "bet", "profit")
		self.txtProfit.setValue(profit)

		result = bd.getValue(self.id, "bet", "result")

		idResutl = {
			"Pendiente": 0,
			"Acertada": 1,
			"Fallada": 2,
			"Nula": 3,
			"Medio Acertada": 4,
			"Medio Fallada": 5,
			"Retirada": 6
		}[result]

		self.cmbResult.setCurrentIndex(idResutl)

		freeBet = bd.getValue(self.id, "bet", "free")
		print(freeBet)
		self.chkFree.setChecked(freeBet)

		bd.close()

		self.setRegion()

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
				index, idCmb = 0, 0
				idBd = bd.getValue(self.id, "bet", "region")
				for i in dataRegion:
					id = i[0]
					if id == idBd:
						idCmb = index
					name = i[1]
					self.cmbRegion.addItem(name)
					self.regionIndexToId[index] = id
					index += 1
				self.cmbRegion.setCurrentIndex(idCmb)
				bd.close()
				self.setCompetition()




	def setCompetition(self):
		self.cmbCompetition.clear()
		bd = Bbdd()

		idRegion = self.regionIndexToId.get(self.cmbRegion.currentIndex())
		idSport = self.sportIndexToId.get(self.cmbSport.currentIndex())

		where = "region=" + str(idRegion) + " AND sport=" + str(idSport)

		data = bd.select("competition", "name", where)

		index, idCmb = 0, 0
		idBd = bd.getValue(self.id, "bet", "competition")

		self.competitionIndexToId = {}
		index = 0
		for i in data:
			id = i[0]
			if id == idBd:
				idCmb = index
			name = i[1]
			self.cmbCompetition.addItem(name)
			self.competitionIndexToId[index] = id
			index += 1

		if index == 0:
			self.btnAccept.setDisabled(True)
		else:
			self.btnAccept.setDisabled(False)


		self.cmbCompetition.setCurrentIndex(idCmb)

		bd.close()


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

		print(self.txtBet.text())
		data.append(str(str_to_float(self.txtProfit.text())))
		data.append(str(str_to_float(self.txtBet.text())))
		data.append(str(str_to_float(self.txtQuota.text())))
		data.append(1 if self.chkFree.isChecked() else 0)

		columns = ["date", "sport", "competition", "region", "player1", "player2", "pick", "bookie", "market",
		           "tipster", "stake", "one", "result", "profit", "bet", "quota", "free"]

		bbdd.update(columns, data, "bet", "id="+self.id)
		bbdd.close()

		QMessageBox.information(self, "Modificada", "Apuesta modificada.")
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

