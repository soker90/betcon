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

		self.setCentralWidget(Bets(self))
		self.insertBet()

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


	def insertBet(self):
		bbdd = Bbdd()

		data = ["9/7/2017", "Futbol", "Mundia", "Mundo", "España", "Italia", "España", "Bet365", "Resultado Final", "", str(3), str(1), "", ""]
		columns = ["date","sport", "competition", "region", "player1", "player2", "pick", "bookie", "market", "tipster", "stake", "one", "result", "profit"]

		#bbdd.insert(columns, data, "bets")
		#bbdd.close()

app = QApplication(sys.argv)
_main = Main()
_main.show()
app.exec_()
