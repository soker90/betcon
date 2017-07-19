import sys
from PyQt5.QtWidgets import QMessageBox, QWidget, QTreeWidgetItem
from PyQt5 import uic

sys.path.append("./lib")
from bookie import Bookie


class Bookies(QWidget):
    def __init__(self, mainWindows):
        QWidget.__init__(self)
        uic.loadUi("../ui/bookies.ui", self)
        self.mainWindows = mainWindows
        mainWindows.aNew.triggered.connect(mainWindows.newBookie)
        self.treeMain.header().hideSection(1)
        self.initTree()
        self.treeMain.itemSelectionChanged.connect(self.changeItem)
        self.mainWindows.aEdit.triggered.connect(self.editItem)
        self.mainWindows.aRemove.triggered.connect(self.deleteItem)

        self.itemSelected = -1

    def initTree(self):
        data = Bookie.selectAll()

        index = 0
        items = []
        for i in data:
            index += 1
            item = QTreeWidgetItem([str(index), str(i.id), i.name])
            items.append(item)

        self.treeMain.addTopLevelItems(items)


    def changeItem(self):
        self.itemSelected = self.treeMain.currentItem().text(1)
        self.mainWindows.enableActions() if int(self.itemSelected) > 7 else self.mainWindows.enableTools()

    def editItem(self):
        self.mainWindows.editBookie(self.itemSelected)

    def deleteItem(self):
        resultado = QMessageBox.question(self, "Eliminar", "¿Estas seguro que desas eliminarlo?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if resultado == QMessageBox.Yes:
            err = Bookie.delete(self.itemSelected)
            if err != 0:
                QMessageBox.critical(self, "Error", "Se ha producido un error al borrar la casa")

            self.mainWindows.setCentralWidget(Bookies(self.mainWindows))
            self.mainWindows.enableTools()

