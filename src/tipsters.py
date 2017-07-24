import sys
from PyQt5.QtWidgets import QMessageBox, QWidget, QTreeWidgetItem
from PyQt5 import uic

sys.path.append("./lib")
from bbdd import Bbdd


class Tipsters(QWidget):
    def __init__(self, mainWindows):
        QWidget.__init__(self)
        uic.loadUi("../ui/tipsters.ui", self)
        self.mainWindows = mainWindows
        mainWindows.aNew.triggered.connect(mainWindows.newTipster)
        self.mainWindows.setWindowTitle("Tipsters | Betcon v" + mainWindows.version)
        self.treeMain.header().hideSection(1)
        self.initTree()

        self.treeMain.itemSelectionChanged.connect(self.changeItem)
        self.mainWindows.aEdit.triggered.connect(self.editItem)
        self.mainWindows.aRemove.triggered.connect(self.deleteItem)
        self.itemSelected = -1

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

    def changeItem(self):
        self.itemSelected = self.treeMain.currentItem().text(1)
        self.mainWindows.enableActions()

    def editItem(self):
        self.mainWindows.editTipster(self.itemSelected)

    def deleteItem(self):
        resultado = QMessageBox.question(self, "Eliminar", "¿Estas seguro que desas eliminar este tipster y todas las apuestas asociadas?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if resultado == QMessageBox.Yes:
            bd = Bbdd()
            bd.delete("tipster", self.itemSelected)
            bd.deleteWhere("bet", "tipster=" + str(self.itemSelected))
            self.mainWindows.setCentralWidget(Tipsters(self.mainWindows))
            self.mainWindows.enableTools()

