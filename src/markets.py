import sys
from PyQt5.QtWidgets import QMessageBox, QWidget, QTreeWidgetItem
from PyQt5 import uic

sys.path.append("./lib")
from bbdd import Bbdd


class Markets(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		uic.loadUi("../ui/markets.ui", self)
		self.mainWindows = mainWindows
		mainWindows.aNew.triggered.connect(mainWindows.newMarket)
		self.mainWindows.setWindowTitle("Mercados | Betcon")
		self.treeMain.header().hideSection(1)
		self.initTree()

		self.treeMain.itemSelectionChanged.connect(self.changeItem)
		self.mainWindows.aEdit.triggered.connect(self.editItem)
		self.mainWindows.aRemove.triggered.connect(self.deleteItem)
		self.itemSelected = -1

	def initTree(self):
		bd = Bbdd()
		data = bd.select("market", "name")

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
		self.mainWindows.editMarket(self.itemSelected)

	def deleteItem(self):
		# TODO Eliminar apuestas asociadas
		resultado = QMessageBox.question(self, "Eliminar", "¿Estas seguro que desas eliminarlo?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if resultado == QMessageBox.Yes:
			bd = Bbdd()
			bd.delete("market", self.itemSelected)
			self.mainWindows.setCentralWidget(Markets(self.mainWindows))
			self.mainWindows.enableTools()

