import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget, QTreeWidgetItem
from PyQt5 import uic

directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")

from bbdd import Bbdd
from func_aux import numberToMonth


class TipstersMonth(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/tipsters_month.ui", self)
		self.mainWindows = mainWindows
		mainWindows.aNew.triggered.connect(mainWindows.newTipsterMonth)
		self.mainWindows.setWindowTitle("Tipsters - Historial de pagos | Betcon v" + mainWindows.version)
		self.treeMain.header().hideSection(0)
		self.treeConjunta.header().hideSection(0)
		self.initTree()

		self.treeMain.itemSelectionChanged.connect(self.changeItem)
		self.treeConjunta.itemSelectionChanged.connect(self.changeItemConjunta)
		self.mainWindows.aEdit.triggered.connect(self.editItem)
		self.mainWindows.aRemove.triggered.connect(self.deleteItem)
		self.mainWindows.enableActionConjunta(False)
		self.itemSelected = -1
		self.itemConjunta = -1

	def initTree(self):
		bd = Bbdd()
		data = bd.select("tipster_month", "year, month")

		items = []
		for i in data:
			id = i[0]
			year = i[2]
			month = numberToMonth(i[1]+1)
			tipster = bd.getValue(i[3], "tipster")
			money = i[4]
			item = QTreeWidgetItem([str(id), str(year), str(month), str(tipster), str(money)])
			items.append(item)

		self.treeMain.addTopLevelItems(items)

		data = bd.select("conjunta", "year, month")

		if len(data) < 1:
			self.lblConjunta.setVisible(False)
			self.treeConjunta.setVisible(False)
		else:
			items = []
			for i in data:
				id = i[0]
				year = i[3]
				month = numberToMonth(i[2] + 1)
				name = i[1]
				money = i[4]
				item = QTreeWidgetItem([str(id), str(year), str(month), str(name), str(money)])
				items.append(item)

			self.treeConjunta.addTopLevelItems(items)

		bd.close()

	def changeItem(self):
		self.itemSelected = self.treeMain.currentItem().text(0)
		self.mainWindows.enableActions()

	def changeItemConjunta(self):
		self.itemConjunta = self.treeConjunta.currentItem().text(0)
		self.mainWindows.enableActionConjunta(True)

	def editItem(self):
		self.mainWindows.editTipsterMonth(self.itemSelected)

	def deleteItem(self):
		resultado = QMessageBox.question(self, "Eliminar",
		                                 "¿Estas seguro que desas eliminar este tipster y todas las apuestas asociadas?",
		                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if resultado == QMessageBox.Yes:
			bd = Bbdd()
			bd.delete("tipster_month", self.itemSelected)
			self.mainWindows.setCentralWidget(TipstersMonth(self.mainWindows))
			self.mainWindows.enableTools("tipster")
			bd.close()
