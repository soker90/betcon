import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget, QGridLayout, QAction
from PyQt5 import uic
from PyQt5.QtCore import Qt
from bets import Bets
from new_bet import NewBet
sys.path.append("./lib")
from bbdd import Bbdd
from regions import Regions
from new_region import NewRegion


class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("../ui/wmain.ui", self)
        self.setWindowTitle("Betcon")
        self.showMaximized()
        self.aNewBet.triggered.connect(self.newBet)
        self.aInicio.triggered.connect(self.home)
        self.aInicio.setEnabled(False)
        self.setCentralWidget(Bets())
        self.insertBet()
        self.setWindowTitle("Inicio | Betcon")
        self.setVisibleTools("bets")
        self.aRegion.triggered.connect(self.regions)
        self.aNewRegion.triggered.connect(self.newRegion)


    def closeEvent(self, event):
        resultado = QMessageBox.question(self, "Salir", "¿Seguro que quieres salir de la aplicación?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if resultado == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def newBet(self):
        self.setCentralWidget(NewBet(self))
        self.enableTools()
        self.aNewBet.setEnabled(False)
        self.setWindowTitle("Nueva Apuesta | Betcon")

    def home(self):
        self.setCentralWidget(Bets())
        self.enableTools()
        self.aInicio.setEnabled(False)
        self.setWindowTitle("Inicio | Betcon")
        self.setVisibleTools("bets")

    def regions(self):
        self.setCentralWidget(Regions(self))
        self.enableTools()
        self.aRegion.setEnabled(False)
        self.setWindowTitle("Regiones | Betcon")
        self.setVisibleTools("regions")

    def newRegion(self):
        self.setCentralWidget(NewRegion(self))
        self.enableTools()
        self.setWindowTitle("Nueva Región | Betcon")

    def enableTools(self):
        self.aNewBet.setEnabled(True)
        self.aInicio.setEnabled(True)
        self.aRegion.setEnabled(True)

    def setVisibleTools(self, type):
        self.toolBet.setVisible(False)
        self.toolRegion.setVisible(False)
        if type == "bets":
            self.toolBet.setVisible(True)
        elif type == "regions":
            self.toolRegion.setVisible(True)

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
