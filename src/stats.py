import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget, QTreeWidgetItem
from PyQt5 import uic
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from libstats import LibStats
from datetime import datetime
from func_aux import key_from_value
from gettext import gettext as _
import gettext


class Stats(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/stats.ui", self)
		gettext.textdomain("betcon")
		gettext.bindtextdomain("betcon", "../lang/mo")
		self.mainWindows = mainWindows
		self.mainWindows.setWindowTitle(_("Stats") + " | Betcon v" + mainWindows.version)
		self.translate()

		self.initData()
		self.cmbYear.activated.connect(self.updateMonths)
		self.cmbMonth.activated.connect(self.updateStats)

	def translate(self):

		self.lblYear.setText(_("Year"))
		self.lblMonth.setText(_("Month"))
		self.lblBalance.setText(_("Balance of the bets of the month"))
		self.lblBet.setText(_("Money Bet"))
		self.lblWinnings.setText(_("Winnings"))
		self.lblLosses.setText(_("Losses"))
		self.lblProfits.setText(_("Profits"))
		self.lblPending.setText(_("Pending"))
		self.lblYield.setText(_("Yield"))
		self.lblQuota.setText(_("Average Quota"))
		self.lblBets.setText(_("Bets"))
		self.lblWon.setText(_("Won"))
		self.lblLost.setText(_("Lost"))
		self.lblNull.setText(_("Null"))
		self.lblSuccess.setText(_("Success"))
		self.lblAverageBet.setText(_("Average Bet"))


	def initData(self):
		self.years, self.months = LibStats.getYears()
		self.cmbYear.addItems(self.years.keys())

		try:
			firstKey = next(iter(self.years))
			self.cmbMonth.addItems(self.getMonths(firstKey))

			self.updateMonths()
		except:
			self.setEnabled(False)

	def updateMonths(self):
		year = self.cmbYear.currentText()
		self.cmbMonth.clear()
		self.cmbMonth.addItems(self.getMonths(year))
		self.updateStats()

	def updateStats(self):
		year = self.cmbYear.currentText()
		sMonth = self.cmbMonth.currentText()
		month = key_from_value(self.months, sMonth)

		data = LibStats.getMonth(year, month)
		self.txtApostado.setText(str(data[0]))
		self.txtGanancias.setText(str(data[1]))
		self.txtPerdidas.setText(str(data[2]))
		self.txtBeneficio.setText(str(data[3]))
		self.txtPendiente.setText(str(data[4]))
		self.txtYield.setText(str(data[5]))
		self.txtCuota.setText(str(data[6]))
		self.txtApuestas.setText(str(data[7]))
		self.txtAciertos.setText(str(data[8]))
		self.txtFallos.setText(str(data[9]))
		self.txtNulos.setText(str(data[10]))
		self.txtAcierto.setText(str(data[11]))
		self.txtApuestaMedia.setText(str(data[12]))


	def getMonths(self, year):
		sMonths = []
		for i in self.years[year]:
			sMonths.append(self.months[i])
		return sMonths




