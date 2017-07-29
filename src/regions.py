import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget, QTreeWidgetItem
from PyQt5 import uic
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from bbdd import Bbdd


class Regions(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/regions.ui", self)
		self.mainWindows = mainWindows
		mainWindows.diconnectActions()
		mainWindows.aNew.triggered.connect(mainWindows.newRegion)
		self.mainWindows.setWindowTitle("Regiones | Betcon v" + mainWindows.version)
		self.treeMain.header().hideSection(1)
		self.initTree()

		self.treeMain.itemSelectionChanged.connect(self.changeItem)
		self.mainWindows.aEdit.triggered.connect(self.editItem)
		self.mainWindows.aRemove.triggered.connect(self.deleteItem)
		self.itemSelected = -1

	def initTree(self):
		bd = Bbdd()
		data = bd.select("region", "name")

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

		bd.close()

	def changeItem(self):
		self.itemSelected = self.treeMain.currentItem().text(1)
		self.mainWindows.enableActions()

	def editItem(self):
		self.mainWindows.editRegion(self.itemSelected)

	def deleteItem(self):
		resultado = QMessageBox.question(self, "Eliminar", "¿Estas seguro que desas eliminar la región y sus competiciones y apuestas asociadas?",
										 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if resultado == QMessageBox.Yes:
			bd = Bbdd()
			bd.delete("region", self.itemSelected)
			bd.deleteWhere("competition", "region=" + str(self.itemSelected))
			bd.deleteWhere("bet", "region=" + str(self.itemSelected))
			self.mainWindows.setCentralWidget(Regions(self.mainWindows))
			self.mainWindows.enableTools()

