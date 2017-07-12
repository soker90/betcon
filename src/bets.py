import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTreeWidgetItem
from PyQt5 import uic

sys.path.append("./lib")
from bbdd import Bbdd

class Bets(QWidget):
    def __init__(self, mainWindows):
        QWidget.__init__(self)
        uic.loadUi("../ui/bets.ui", self)
        self.mainWindows = mainWindows
        mainWindows.aNew.triggered.connect(mainWindows.newBet)
        self.treeMain.header().hideSection(1)
        self.initTree()

    def initTree(self):
        bd = Bbdd()
        data = bd.select("bet", "date DESC")

        index = 0
        items = []
        for i in data:
            index += 1
            id = i[0]
            date = i[1]
            sport = bd.getValue(i[2], "sport")
            competition = bd.getValue(i[3], "competition")
            region = bd.getValue(i[4], "region")
            player1 = i[5]
            player2 = i[6]
            pick = i[7]
            bookie = bd.getValue(i[8], "bookie")
            market = bd.getValue(i[9], "market")
            tipster = bd.getValue(i[10], "tipster")
            stake = i[11]
            one = i[12]
            result = bd.getValue(i[13], "result")
            profit = i[14]
            bet = i[15]
            quota = i[16]
            item = QTreeWidgetItem([str(index), str(id), str(date), str(sport), str(competition), str(region), player1,
                                    player2, pick, bookie, market, tipster, stake, one, bet, quota, result, profit])
            items.append(item)

        self.treeMain.addTopLevelItems(items)

        bd.close()


