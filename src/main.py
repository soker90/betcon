import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget, QGridLayout, QAction
from PyQt5 import uic
from PyQt5.QtCore import Qt
from principal import Principal
from new_bet import NewBet
sys.path.append("./lib")
from bbdd import Bbdd


class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("../qt/wmain.ui", self)
        self.setWindowTitle("Betcon")
        self.showMaximized()
        self.aApuesta.triggered.connect(self.newBet)
        self.aInicio.triggered.connect(self.home)
        self.aInicio.setEnabled(False)
        self.setCentralWidget(Principal())
        self.insertBet()
        self.setWindowTitle("Inicio | Betcon")


    def closeEvent(self, event):
        resultado = QMessageBox.question(self, "Salir", "¿Seguro que quieres salir de la aplicación?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if resultado == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def newBet(self):
        self.setCentralWidget(NewBet(self))
        self.aInicio.setEnabled(True)
        self.aApuesta.setEnabled(False)
        self.setWindowTitle("Nueva Apuesta | Betcon")

    def home(self):
        self.setCentralWidget(Principal())
        self.aApuesta.setEnabled(True)
        self.aInicio.setEnabled(False)
        self.setWindowTitle("Inicio | Betcon")

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
