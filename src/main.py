import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QComboBox, QGridLayout, QAction
from PyQt5 import uic
from PyQt5.QtCore import Qt
from bets import Bets
from new_bet import NewBet
sys.path.append("./lib")
from regions import Regions
from new_region import NewRegion
from competitions import Competitions
from new_competition import NewCompetition
from sports import Sports
from new_sport import NewSport
from bookies import Bookies
from new_bookie import NewBookie
from markets import Markets
from new_market import NewMarket
from tipsters import Tipsters
from new_tipster import NewTipster
from edit_bet import EditBet
from edit_bookie import EditBookie
from edit_competition import EditCompetition
from edit_tipster import EditTipster
from edit_market import EditMarket
from edit_region import EditRegion
from edit_sport import EditSport
from stats import Stats
from banks import Banks
from bonus import Bonus
from new_bank import NewBank
from stats_tipster import StatsTipster
from stats_bookie import StatsBookie
from stats_market import StatsMarket
from stats_region import StatsRegion
from stats_sport import StatsSport
from stats_stake import StatsStake
from add_money import AddMoney
from new_bonus import NewBonus
from edit_bonus import EditBonus


class Main(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		uic.loadUi("../ui/wmain.ui", self)
		self.showMaximized()
		self.enableTools()

		archivo = open("version.txt")
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

		self.aStatsGeneral.triggered.connect(self.stats)
		self.aStatsTipster.triggered.connect(self.statsTipster)
		self.aStatsBookie.triggered.connect(self.statsBookie)
		self.aStatsMarket.triggered.connect(self.statsMarket)
		self.aStatsRegion.triggered.connect(self.statsRegion)
		self.aStatsSport.triggered.connect(self.statsSport)
		self.aStatsStake.triggered.connect(self.statsStake)

		self.aAddMoney.triggered.connect(self.addMoney)
		self.aClose.triggered.connect(self.close)

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
		self.enableTools()

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
		self.enableTools()

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

	#Auxiliary Functions

	def enableTools(self, type=None):
		self.toolBank.setVisible(False)
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

	def enableActions(self, edit=True):
		if edit:
			self.aEdit.setEnabled(True)
		self.aRemove.setEnabled(True)


	#Events

	def closeEvent(self, event):
		resultado = QMessageBox.question(self, "Salir", "¿Seguro que quieres salir de la aplicación?",
										 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if resultado == QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()


app = QApplication(sys.argv)
_main = Main()
_main.show()
app.exec_()
