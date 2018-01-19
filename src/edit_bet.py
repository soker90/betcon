import sys, os, inspect
from datetime import datetime
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QWidget, QComboBox, QAction, QPushButton, QShortcut, QHBoxLayout, QLayout, QDateTimeEdit
from PyQt5 import uic
from bets import Bets
from PyQt5.QtCore import QDateTime
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from bbdd import Bbdd
from func_aux import str_to_float, str_to_bool, key_from_value
from gettext import gettext as _
import gettext
from new_bet import NewBet


class EditBet(QWidget):
	def __init__(self, mainWindows, id):
		QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/new_bet.ui", self)
		gettext.textdomain("betcon")
		gettext.bindtextdomain("betcon", "../lang/mo")
		self.mainWindows = mainWindows
		self.mainWindows.setWindowTitle(_("Modify Bet") + " | Betcon v" + mainWindows.version)
		self.btnAccept.clicked.connect(self.accept)
		self.btnCancel.clicked.connect(self.cancel)
		self.btnAdd.clicked.connect(self.addCombined)
		self.id = id
		self.initData()
		self.cmbRegion.activated.connect(self.setCompetition)
		self.cmbSport.activated.connect(self.setRegion)
		self.cmbResult.activated.connect(self.updateProfit)
		self.cmbMarket.activated.connect(self.combined)
		self.txtQuota.valueChanged.connect(self.updateProfit)
		self.txtBet.valueChanged.connect(self.updateProfit)
		self.chkFree.clicked.connect(self.freeBet)
		self.txtStake.valueChanged.connect(self.updateBet)
		self.txtOne.valueChanged.connect(self.updateBet)

		self.combined()
		self.initCombined()
		NewBet.translate(self)


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

		self.players = bd.executeQuery(
			"SELECT player1 AS player FROM bet UNION SELECT player2 AS player FROM bet ORDER BY player")
		self.players = [row[0] for row in self.players]

		self.txtPlayer1.addItems(self.players)
		self.txtPlayer2.addItems(self.players)

		# txtPlayer1
		player1 = bd.getValue(self.id, "bet", "player1")
		self.txtPlayer1.setCurrentText(player1)

		# txtPlayer2
		player2 = bd.getValue(self.id, "bet", "player2")
		self.txtPlayer2.setCurrentText(player2)

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

		self.cmbResult.setCurrentIndex(int(result))

		freeBet = bd.getValue(self.id, "bet", "free")

		self.chkFree.setChecked(freeBet)


		bd.close()

		self.setRegion()

		# Combined
		self.contComb = 0
		self.dates = []
		self.sports = []
		self.regions = []
		self.competitions = []
		self.players1 = []
		self.players2 = []
		self.picks = []
		self.results = []
		self.buttons = []

		self.regionIndexToIdCmb = []
		self.competitionIndexToIdCmb = []

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

		data.append(self.txtPlayer1.currentText())
		data.append(self.txtPlayer2.currentText())
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
		data.append(self.cmbResult.currentIndex())

		print(self.txtBet.text())
		data.append(str(str_to_float(self.txtProfit.text())))
		data.append(str(str_to_float(self.txtBet.text())))
		data.append(str(str_to_float(self.txtQuota.text())))
		data.append(1 if self.chkFree.isChecked() else 0)

		columns = ["date", "sport", "competition", "region", "player1", "player2", "pick", "bookie", "market",
		           "tipster", "stake", "one", "result", "profit", "bet", "quota", "free"]

		bbdd.update(columns, data, "bet", "id="+self.id)

		if self.cmbMarket.currentText() == "Combinada":
			columns = ["bet", "date", "sport", "competition", "region", "player1", "player2", "pick", "result"]
			bbdd.deleteWhere("combined", "bet=" + str(self.id))

			for i in range(0, self.contComb):
				data = []
				data.append(self.id)
				data.append(self.dates[i].dateTime().toPyDateTime())
				idSport = self.sportIndexToId.get(self.sports[i].currentIndex())
				data.append(idSport)
				idCompetition = self.competitionIndexToIdCmb[i].get(self.competitions[i].currentIndex())
				data.append(idCompetition)
				idRegion = self.regionIndexToIdCmb[i].get(self.regions[i].currentIndex())
				data.append(idRegion)
				data.append(self.players1[i].currentText())
				data.append(self.players2[i].currentText())
				data.append(self.picks[i].text())
				data.append(self.results[i].currentText())
				bbdd.insert(columns, data, "combined")

		bbdd.close()

		QMessageBox.information(self, _("Modified"), _("Modified bet."))
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

	def addCombined(self):
		self.dates.append(QDateTimeEdit())
		sDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		date = QDateTime.fromString(sDate, "yyyy-MM-dd hh:mm:ss")
		self.dates[self.contComb].setDateTime(date)
		self.dates[self.contComb].setMaximumSize(120, 50)
		self.pnlDate.addWidget(self.dates[self.contComb])

		self.sports.append(QComboBox())
		self.sports[self.contComb].setModel(self.cmbSport.model())
		self.regionIndexToIdCmb.append({})
		cont = self.contComb
		self.sports[self.contComb].activated.connect(lambda: self.setRegionComb(cont))
		self.pnlSport.addWidget(self.sports[self.contComb])

		self.regions.append(QComboBox())
		self.competitionIndexToIdCmb.append({})
		self.regions[self.contComb].activated.connect(lambda: self.setCompetitionComb(cont))
		self.pnlRegion.addWidget(self.regions[self.contComb])

		self.competitions.append(QComboBox())
		self.pnlCompetition.addWidget(self.competitions[self.contComb])
		self.players1.append(QComboBox())
		self.players1[self.contComb].setEditable(True)
		self.players1[self.contComb].addItems(self.players)
		self.players1[self.contComb].setMaximumSize(200, 50)
		self.pnlPlayer1.addWidget(self.players1[self.contComb])
		self.players2.append(QComboBox())
		self.players2[self.contComb].setEditable(True)
		self.players2[self.contComb].addItems(self.players)
		self.players2[self.contComb].setMaximumSize(200, 50)
		self.pnlPlayer2.addWidget(self.players2[self.contComb])
		self.picks.append(QLineEdit())
		self.picks[self.contComb].setMaximumSize(200, 50)
		self.pnlPick.addWidget(self.picks[self.contComb])
		self.results.append(QComboBox())
		self.results[self.contComb].addItems(["Pendiente", "Acertada", "Fallada", "Nula", "Medio Acertada", "Medio Fallada", "Retirada"])
		self.pnlResult.addWidget(self.results[self.contComb])
		self.buttons.append(QPushButton())
		self.buttons[self.contComb].setText("X")
		self.buttons[self.contComb].setStyleSheet("color:red; font-weight: bold;")
		self.buttons[self.contComb].setMaximumSize(50, 50)
		self.buttons[self.contComb].clicked.connect(lambda: self.removeRow(cont))
		self.pnlButton.addWidget(self.buttons[self.contComb])

		self.contComb += 1
		if self.contComb == 10:
			self.btnAdd.setEnabled(False)

	def setCombinedVisible(self, visible):
		self.btnAdd.setVisible(visible)
		self.lblDate.setVisible(visible)
		self.lblSport.setVisible(visible)
		self.lblRegion.setVisible(visible)
		self.lblCompetition.setVisible(visible)
		self.lblPlayer1.setVisible(visible)
		self.lblPlayer2.setVisible(visible)
		self.lblResult.setVisible(visible)
		self.lblPick.setVisible(visible)
		for i in range(self.contComb):
			self.dates[i].setVisible(visible)
			self.sports[i].setVisible(visible)
			self.competitions[i].setVisible(visible)
			self.regions[i].setVisible(visible)
			self.players1[i].setVisible(visible)
			self.players2[i].setVisible(visible)
			self.picks[i].setVisible(visible)
			self.results[i].setVisible(visible)
			self.buttons[i].setVisible(visible)

	def combined(self):
		if self.cmbMarket.currentText() == "Combinada":
			self.setCombinedVisible(True)
		else:
			self.setCombinedVisible(False)

	def removeRow(self, index):
		# TODO: FIX THIS!!
		obj1 = self.dates.pop(index)
		self.pnlDate.removeWidget(obj1)
		obj1.setVisible(False)
		obj2 = self.sports.pop(index)
		self.pnlSport.removeWidget(obj2)
		obj2.setVisible(False)
		obj3 = self.regions.pop(index)
		self.pnlRegion.removeWidget(obj3)
		obj3.setVisible(False)
		obj4 = self.competitions.pop(index)
		self.pnlCompetition.removeWidget(obj4)
		obj4.setVisible(False)
		obj5 = self.players1.pop(index)
		self.pnlPlayer1.removeWidget(obj5)
		obj5.setVisible(False)
		obj6 = self.players2.pop(index)
		self.pnlPlayer2.removeWidget(obj6)
		obj6.setVisible(False)
		obj7 = self.picks.pop(index)
		self.pnlPick.removeWidget(obj7)
		obj7.setVisible(False)
		obj8 = self.results.pop(index)
		self.pnlResult.removeWidget(obj8)
		obj8.setVisible(False)
		obj9 = self.buttons.pop(index)
		self.pnlButton.removeWidget(obj9)
		obj9.setVisible(False)

		self.contComb -= 1

		for i in range(self.contComb):
			self.pnlButton.removeWidget(self.buttons[i])
			self.buttons[i].disconnect()
			self.buttons[i].clicked.connect(lambda: self.removeRow(i))
			self.pnlButton.addWidget(self.buttons[i])

		if self.contComb == 9:
			self.btnAdd.setEnabled(True)

	def setCompetitionComb(self, index_cmb):
		self.competitions[index_cmb].clear()
		bd = Bbdd()

		idRegion = self.regionIndexToIdCmb[index_cmb].get(self.regions[index_cmb].currentIndex())
		idSport = self.sportIndexToId.get(self.sports[index_cmb].currentIndex())

		where = "region=" + str(idRegion) + " AND sport=" + str(idSport)

		try:
			data = bd.select("competition", "name", where)

			index = 0
			self.competitionIndexToIdCmb[index_cmb] = {}
			for i in data:
				id = i[0]
				name = i[1]
				self.competitions[index_cmb].addItem(name)
				self.competitionIndexToIdCmb[index_cmb][index] = id
				index += 1

			if index == 0:
				self.btnAccept.setDisabled(True)
			else:
				self.btnAccept.setDisabled(False)
		except:
			self.btnAccept.setDisabled(True)
		bd.close()


	def setRegionComb(self, index_cmb):
		print(index_cmb)
		self.btnAccept.setDisabled(False)
		self.regions[index_cmb].clear()
		bd = Bbdd()

		idSport = self.sportIndexToId.get(self.sports[index_cmb].currentIndex())

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
				j += 1

			where = " id in "+sData
			dataRegion = bd.select("region", "name", where)

			if len(dataRegion) < 1:
				self.btnAccept.setDisabled(True)
				bd.close()
			else:
				self.regionIndexToIdCmb[index_cmb] = {}
				index = 0
				for i in dataRegion:
					id = i[0]
					name = i[1]
					self.regions[index_cmb].addItem(name)
					self.regionIndexToIdCmb[index_cmb][index] = id
					index += 1
				bd.close()
				self.setCompetitionComb(index_cmb)

		else:
			self.btnAccept.setDisabled(True)
			bd.close()

		if len(data) == 0 or len(dataRegion):
			self.btnAccept.setDisabled(True)
		else:
			self.btnAccept.setDisabled(False)

	def initCombined(self):
		bd = Bbdd()
		data = bd.select("combined", None, "bet=" + str(self.id))
		i = 0
		for bet in data:
			self.addCombined()
			date = QDateTime.fromString(bet[2], "yyyy-MM-dd hh:mm:ss")
			self.dates[i].setDateTime(date)
			sport = key_from_value(self.sportIndexToId, bet[3])
			self.sports[i].setCurrentIndex(sport)
			self.setRegionComb(i)
			region = key_from_value(self.regionIndexToIdCmb[i], bet[5])
			self.regions[i].setCurrentIndex(region)
			self.setCompetitionComb(i)
			competition = key_from_value(self.competitionIndexToIdCmb[i], bet[4])
			self.competitions[i].setCurrentIndex(competition)
			self.players1[i].setCurrentText(bet[6])
			self.players2[i].setCurrentText(bet[7])
			self.picks[i].setText(bet[8])

			result = {
				"Pendiente": 0,
				"Acertada": 1,
				"Fallada": 2,
				"Nula": 3,
				"Medio Acertada": 4,
				"Medio Fallada": 5,
				"Retirada": 6
			}[bet[9]]

			self.results[i].setCurrentIndex(result)
			i += 1

		bd.close()

