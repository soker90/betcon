import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTreeWidgetItem
from PyQt5 import uic

sys.path.append("./lib")
from bbdd import Bbdd


class Tipsters(QWidget):
    def __init__(self, mainWindows):
        QWidget.__init__(self)
        uic.loadUi("../ui/tipsters.ui", self)
        self.mainWindows = mainWindows
        mainWindows.aNew.triggered.connect(mainWindows.newTipster)
        self.treeMain.header().hideSection(1)
        self.initTree()

    def initTree(self):
        bd = Bbdd()
        data = bd.select("tipster", "name")

        index = 0
        items = []
        for i in data:
            index += 1
            id = i[0]
            name = i[1]
            item = QTreeWidgetItem([str(index), str(id), name])
            items.append(item)

        self.treeMain.addTopLevelItems(items)

        bd.close()

