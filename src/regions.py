import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTreeWidgetItem
from PyQt5 import uic

sys.path.append("./lib")
from bbdd import Bbdd


class Regions(QWidget):
    def __init__(self, mainWindows):
        QWidget.__init__(self)
        uic.loadUi("../ui/regions.ui", self)
        self.mainWindows = mainWindows
        self.mainWindows.setWindowTitle("Zonas | Betcon")
        self.treeMain.header().hideSection(1)
        self.initTree()

    def initTree(self):
        bd = Bbdd()
        data = bd.select("region","name")

        index = 0
        items = []
        for i in data:
            index += 1
            id = i[0]
            name = i[1]
            competitions = bd.count("competition", "region="+str(id))
            item = QTreeWidgetItem([str(index), str(id), name, str(competitions)])
            items.append(item)

        self.treeMain.addTopLevelItems(items)





        #self.cmbSport.model().sort(0)

        bd.close()

