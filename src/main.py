import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QComboBox, QGridLayout, QAction
from PyQt5 import uic
from PyQt5.QtCore import Qt
from bets import Bets
from new_bet import NewBet
sys.path.append("./lib")
from bbdd import Bbdd
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


class Main(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		uic.loadUi("../ui/wmain.ui", self)
		self.showMaximized()
		self.setWindowTitle("Inicio | Betcon")

		self.aInicio.triggered.connect(self.home)
		self.aRegion.triggered.connect(self.regions)
		self.aCompetition.triggered.connect(self.competitions)
		self.aSport.triggered.connect(self.sports)
		self.aBookie.triggered.connect(self.bookies)
		self.aMarket.triggered.connect(self.markets)
		self.aTipster.triggered.connect(self.tipsters)

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

	#ToolSecundary

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


	#Auxiliary Functions

	def enableTools(self):
		self.toolSecondary.setVisible(True)

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
