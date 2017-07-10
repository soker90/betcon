import sys
from PyQt5.QtWidgets import QComboBox, QMessageBox, QWidget, QGridLayout, QAction, QPushButton, QShortcut
from PyQt5 import uic
from PyQt5.QtCore import QDateTime, QVariant
from bets import Bets
sys.path.append("./lib")
from bbdd import Bbdd

class NewBet(QWidget):
    def __init__(self, mainWindows):
        QWidget.__init__(self)
        uic.loadUi("../ui/new_bet.ui", self)
        self.mainWindows = mainWindows
        self.btnAccept.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.cancel)
        self.initData()



    def initData(self):
        #dtDate
        curent_t = QDateTime().currentDateTime()
        self.dtDate.setDateTime(curent_t)

        #cmbSport
        bd = Bbdd()
        data = bd.select("sport")

        for i in data:
            index = i[0]
            name = i[1]
            self.cmbSport.insertItem(index, name)

        self.cmbSport.model().sort(0)




        bd.close()






    def close(self):
            self.mainWindows.setCentralWidget(Bets())
            self.mainWindows.aApuesta.setEnabled(True)
            self.mainWindows.aInicio.setEnabled(False)
            self.mainWindows.setWindowTitle("Inicio | Betcon")

    def cancel(self):
        self.close()

    def accept(self):
        datos = []

        bbdd = Bbdd()

        #dtDate
        datos.append(self.dtDate.dateTime().toPyDateTime())

        date = self.dtDate.dateTime().toPyDateTime()
        datos.append(date)

        #cmbSport
        datos.append(self.cmbSport.currentIndex())


        sport = self.cmbSport.currentIndex()

        data = [date, sport, "Mundia", "Mundo", "España", "Italia", "España", "Bet365", "Resultado Final", "",
                str(3), str(1), "", ""]
        columns = ["date", "sport", "competition", "region", "player1", "player2", "pick", "bookie", "market",
                   "tipster", "stake", "one", "result", "profit"]


        bbdd.insert(columns, data, "bets")
        bbdd.close()


        QMessageBox.information(self, "Añadida", "Nueva apuesta añadida.")
        self.close()

