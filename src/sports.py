import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTreeWidgetItem
from PyQt5 import uic

sys.path.append("./lib")
from bbdd import Bbdd


class Sports(QWidget):
    def __init__(self, mainWindows):
        QWidget.__init__(self)
        uic.loadUi("../ui/sports.ui", self)
        self.mainWindows = mainWindows
        mainWindows.aNew.triggered.connect(mainWindows.newSport)
        self.treeMain.header().hideSection(1)
        self.initTree()

    def initTree(self):
        bd = Bbdd()
        data = bd.select("sport", "name")

        index = 0
        items = []
        for i in data:
            index += 1
            id = i[0]
            name = i[1]
            competitions = bd.count("competition", "sport="+str(id))
            item = QTreeWidgetItem([str(index), str(id), name, str(competitions)])
            items.append(item)

        self.treeMain.addTopLevelItems(items)

        bd.close()

