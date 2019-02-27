import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5 import uic

from new_conjunta import NewConjunta

directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from bbdd import Bbdd
from tipsters_month import TipstersMonth
from gettext import gettext as _
import gettext

class EditConjunta(QWidget):
	def __init__(self, mainWindows, id):
		QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/new_conjunta.ui", self)
		gettext.textdomain("betcon")
		gettext.bindtextdomain("betcon", "../lang/mo" + mainWindows.lang)
		gettext.bindtextdomain("betcon", "/usr/share/locale" + mainWindows.lang)
		self.mainWindows = mainWindows
		self.btnAccept.clicked.connect(self.accept)
		self.btnCancel.clicked.connect(self.cancel)
		self.btnAdd.clicked.connect(self.add)
		self.btnDel.clicked.connect(self.delete)
		self.mainWindows.setWindowTitle(_("Update joint purchase") + " | Betcon v" + mainWindows.version)

		self.id = id
		self.selected = [0, 1]
		self.initData()
		NewConjunta.translate(self)
		self.listFree.itemSelectionChanged.connect(self.updateEnableButton)
		self.listSelected.itemSelectionChanged.connect(self.updateEnableButton)


	def initData(self):

		bd = Bbdd()
		data = bd.select("conjunta", None, "id=" + str(self.id))[0]

		self.txtName.setText(data[1])
		self.txtYear.setValue(data[3])
		self.cmbMonth.setCurrentIndex(data[2])
		self.txtMoney.setValue(data[4])


		data = bd.select("conjunta_tipster", None, "conjunta=" + str(self.id), "tipster")

		for i in data:
			self.selected.append(i[0])
		bd.close()
		self.updateData()

	def updateData(self):

		bd = Bbdd()

		data = bd.select("tipster", "name")

		self.listFree.clear()
		self.listSelected.clear()

		self.tipsterIndexToId = {}
		self.selectedIndexToId = {}
		index, index2 = 0, 0
		for i in data:
			id = i[0]
			if id == 1:
				continue
			name = i[1]
			if id in self.selected:
				self.listSelected.addItem(name)
				self.selectedIndexToId[index2] = id
				index2 += 1
			else:
				self.listFree.addItem(name)
				self.tipsterIndexToId[index] = id
				index += 1

		bd.close()
		self.updateEnableButton()

	def close(self):
			self.mainWindows.setCentralWidget(TipstersMonth(self.mainWindows))

	def cancel(self):
		self.close()

	def updateEnableButton(self):
		if self.listFree.count() == 0 or self.listFree.currentRow() == -1:
			self.btnAdd.setEnabled(False)
		else:
			self.btnAdd.setEnabled(True)

		if self.listSelected.count() == 0 or self.listSelected.currentRow() == -1:
			self.btnDel.setEnabled(False)
		else:
			self.btnDel.setEnabled(True)

	def accept(self):
		money = str(self.txtMoney.text())
		data = [self.cmbMonth.currentIndex(), self.txtYear.text(), self.txtName.text(), money]
		columns = ["month", "year", "name", "money"]

		bbdd = Bbdd()
		bbdd.update(columns, data, "conjunta", "id=" + str(self.id))

		bbdd.deleteWhere("conjunta_tipster", "conjunta=" + str(self.id))

		for i in self.selected:
			if i in (0, 1):
				continue
			bbdd.insert(["conjunta", "tipster"], [self.id, i], "conjunta_tipster")

		bbdd.close()


		QMessageBox.information(self, _("Added"), _("New joint purchase added."))

		self.close()

	def add(self):
		idTipster = self.tipsterIndexToId.get(self.listFree.currentRow())
		self.selected.append(idTipster)
		self.updateData()

	def delete(self):
		idTipster = self.selectedIndexToId.get(self.listSelected.currentRow())
		self.selected.remove(idTipster)
		self.updateData()


