import inspect
import os
import sys

directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog
from PyQt5 import uic
sys.path.append(directory)
from src.bets import Bets
from src.new_bet import NewBet
sys.path.append(directory + "/lib")
from src.regions import Regions
from src.new_region import NewRegion
from src.competitions import Competitions
from src.new_competition import NewCompetition
from src.sports import Sports
from src.new_sport import NewSport
from src.bookies import Bookies
from src.new_bookie import NewBookie
from src.markets import Markets
from src.new_market import NewMarket
from src.tipsters import Tipsters
from src.new_tipster import NewTipster
from src.edit_bet import EditBet
from src.edit_bookie import EditBookie
from src.edit_competition import EditCompetition
from src.edit_tipster import EditTipster
from src.edit_market import EditMarket
from src.edit_region import EditRegion
from src.edit_sport import EditSport
from src.stats import Stats
from src.banks import Banks
from src.bonus import Bonus
from src.new_bank import NewBank
from src.stats_tipster import StatsTipster
from src.stats_bookie import StatsBookie
from src.stats_market import StatsMarket
from src.stats_region import StatsRegion
from src.stats_sport import StatsSport
from src.stats_stake import StatsStake
from src.add_money import AddMoney
from src.new_bonus import NewBonus
from src.edit_bonus import EditBonus
from src.new_tipster_month import NewTipsterMonth
from src.tipsters_month import TipstersMonth
from src.edit_tipster_month import EditTipsterMonth
from src.new_conjunta import NewConjunta
from src.edit_conjunta import EditConjunta


class Main(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		uic.loadUi(directory + "/../ui/wmain.ui", self)
		self.showMaximized()
		self.enableTools()

		archivo = open(directory+"/version.txt")
		self.version = archivo.readline()
		self.setWindowTitle("Inicio | Betcon v" + self.version)

		self.aInicio.triggered.connect(self.home)
		self.aRegion.triggered.connect(self.regions)
		self.aCompetition.triggered.connect(self.competitions)
		self.aSport.triggered.connect(self.sports)
		self.aBookie.triggered.connect(self.bookies)
		self.aMarket.triggered.connect(self.markets)
		self.aTipster.triggered.connect(self.tipsters)
		self.aStat.triggered.connect(self.stats)
		self.aBank.triggered.connect(self.banks)
		self.aBonus.triggered.connect(self.bonus)
		self.aTipsterMonth.triggered.connect(self.tipstersMonth)

		self.aStatsGeneral.triggered.connect(self.stats)
		self.aStatsTipster.triggered.connect(self.statsTipster)
		self.aStatsBookie.triggered.connect(self.statsBookie)
		self.aStatsMarket.triggered.connect(self.statsMarket)
		self.aStatsRegion.triggered.connect(self.statsRegion)
		self.aStatsSport.triggered.connect(self.statsSport)
		self.aStatsStake.triggered.connect(self.statsStake)

		self.aAddMoney.triggered.connect(self.addMoney)
		self.aClose.triggered.connect(self.close)
		self.aAbout.triggered.connect(self.about)

		self.aNewConjunta.triggered.connect(self.newConjunta)

		self.setCentralWidget(Bets(self))



	#ToolPrimary

	def home(self):
		self.setCentralWidget(Bets(self))
		self.enableTools()

	def regions(self):
		self.setCentralWidget(Regions(self))
		self.enableTools()

	def competitions(self):
		self.setCentralWidget(Competitions(self))
		self.enableTools()

	def sports(self):
		self.setCentralWidget(Sports(self))
		self.enableTools()

	def bookies(self):
		self.setCentralWidget(Bookies(self))
		self.enableTools()

	def markets(self):
		self.setCentralWidget(Markets(self))
		self.enableTools()

	def tipsters(self):
		self.setCentralWidget(Tipsters(self))
		self.enableTools("tipster")

	def tipstersMonth(self):
		self.setCentralWidget(TipstersMonth(self))
		self.enableTools("tipster_money")

	def stats(self):
		self.setCentralWidget(Stats(self))
		self.enableTools("stats")

	def banks(self):
		self.setCentralWidget(Banks(self))
		self.enableTools("bank")

	def bonus(self):
		self.setCentralWidget(Bonus(self))
		self.enableTools()

	# ToolSecundary
	# New Buttons

	def newBet(self):
		self.setCentralWidget(NewBet(self))
		self.enableTools()

	def newRegion(self):
		self.setCentralWidget(NewRegion(self))
		self.enableTools()

	def newCompetition(self):
		self.setCentralWidget(NewCompetition(self))
		self.enableTools()

	def newSport(self):
		self.setCentralWidget(NewSport(self))
		self.enableTools()

	def newBookie(self):
		self.setCentralWidget(NewBookie(self))
		self.enableTools()

	def newMarket(self):
		self.setCentralWidget(NewMarket(self))
		self.enableTools()

	def newTipster(self):
		self.setCentralWidget(NewTipster(self))
		self.enableTools("tipster")

	def newTipsterMonth(self):
		self.setCentralWidget(NewTipsterMonth(self))
		self.enableTools("tipster")

	def newBank(self):
		self.setCentralWidget(NewBank(self))
		self.enableTools("bank")

	def newBonus(self):
		self.setCentralWidget(NewBonus(self))
		self.enableTools()

	# Edit Buttons

	def editBet(self, id):
		self.setCentralWidget(EditBet(self, id))
		self.enableTools()

	def editRegion(self, id):
		self.setCentralWidget(EditRegion(self, id))
		self.enableTools()

	def editCompetition(self, id):
		self.setCentralWidget(EditCompetition(self, id))
		self.enableTools()

	def editSport(self, id):
		self.setCentralWidget(EditSport(self, id))
		self.enableTools()

	def editBookie(self, id):
		self.setCentralWidget(EditBookie(self, id))
		self.enableTools()

	def editMarket(self, id):
		self.setCentralWidget(EditMarket(self, id))
		self.enableTools()

	def editTipster(self, id):
		self.setCentralWidget(EditTipster(self, id))
		self.enableTools()

	def editTipsterMonth(self, id):
		self.setCentralWidget(EditTipsterMonth(self, id))
		self.enableTools("tipster")

	def editBonus(self, id):
		self.setCentralWidget(EditBonus(self, id))
		self.enableTools()

	# Stats

	def statsTipster(self):
		self.setCentralWidget(StatsTipster(self))

	def statsBookie(self):
		self.setCentralWidget(StatsBookie(self))

	def statsMarket(self):
		self.setCentralWidget(StatsMarket(self))

	def statsRegion(self):
		self.setCentralWidget(StatsRegion(self))

	def statsSport(self):
		self.setCentralWidget(StatsSport(self))

	def statsStake(self):
		self.setCentralWidget(StatsStake(self))

	# Bank

	def addMoney(self):
		self.setCentralWidget(AddMoney(self))

	# Conjunta
	def newConjunta(self):
		self.setCentralWidget(NewConjunta(self))

	def editConjunta(self, id):
		self.setCentralWidget(EditConjunta(self, id))
		self.enableActionConjunta(False)

	#Auxiliary Functions

	def enableTools(self, type=None):
		self.toolBank.setVisible(False)
		self.toolTipster.setVisible(False)
		self.toolConjunta.setVisible(False)
		if type is "stats":
			self.toolSecondary.setVisible(False)
			self.toolStat.setVisible(True)
		else:
			self.toolSecondary.setVisible(True)
			self.toolStat.setVisible(False)
			self.aEdit.setEnabled(False)
			self.aRemove.setEnabled(False)
			if type is "bank":
				self.toolBank.setVisible(True)
			if type is "tipster":
				self.toolTipster.setVisible(True)
			if type is "tipster_money":
				self.toolTipster.setVisible(True)
				self.toolConjunta.setVisible(True)

	def enableActions(self, edit=True):
		if edit:
			self.aEdit.setEnabled(True)
		self.aRemove.setEnabled(True)

	def enableActionConjunta(self, enable):
		self.aEditConjunta.setEnabled(enable)
		self.aDeleteConjunta.setEnabled(enable)

	def diconnectActions(self):
		try:
			self.aNew.triggered.disconnect()
		except:
			pass
		try:
			self.aEdit.triggered.disconnect()
		except:
			pass
		try:
			self.aRemove.triggered.disconnect()
		except:
			pass


	#Events

	def closeEvent(self, event):
		resultado = QMessageBox.question(self, "Salir", "¿Seguro que quieres salir de la aplicación?",
										 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if resultado == QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()


	def about(self):
		about = About()
		about.exec_()

class About(QDialog):
	def __init__(self):
		QDialog.__init__(self)
		uic.loadUi(directory + "/../ui/about.ui", self)
		archivo = open(directory + "/version.txt")
		version = archivo.readline()
		self.setWindowTitle("Acerca de")
		self.txtText.setHtml("<p style='text-align: center;'><br>Betcon v" + version + "<p/>" \
		                     "<p style='text-align: center;'>Web: https://soker90.github.io/betcon/<p/>" \
		                     "<p style='text-align: center;'>Creado por Eduardo Parra Mazuecos<p/>" \
		                     "<p style='text-align: center;'>Contacto: eduparra90@gmail.com</p>" \
		                     "<p style='text-align: center;'>Licencia GPLv3<p/>")


app = QApplication(sys.argv)
_main = Main()
_main.show()
app.exec_()
