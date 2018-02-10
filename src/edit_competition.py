import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget, QComboBox
from PyQt5 import uic

from new_competition import NewCompetition

directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from bbdd import Bbdd
from competitions import Competitions
from gettext import gettext as _
import gettext

class EditCompetition(QWidget):
	def __init__(self, mainWindows, id):
		QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/new_competition.ui", self)
		gettext.textdomain("betcon")
		gettext.bindtextdomain("betcon", "../lang/mo")
		self.mainWindows = mainWindows
		self.btnAccept.clicked.connect(self.accept)
		self.btnCancel.clicked.connect(self.cancel)
		self.mainWindows.setWindowTitle(_("Modify Competition") + " | Betcon v" + mainWindows.version)
		self.txtName.returnPressed.connect(self.btnAccept.click)

		self.id = id
		self.initData()
		NewCompetition.translate(self)

	def initData(self):
		bd = Bbdd()
		# txtName
		name = bd.getValue(self.id, "competition")
		self.txtName.setText(name)

		# cmbRegion
		data = bd.select("region", "name")

		self.regionIndexToId = {}
		index, idCmb = 0, 0
		idBd = bd.getValue(self.id, "competition", "region")
		for i in data:
			id = i[0]
			if id == idBd:
				idCmb = index
			name = i[1]
			self.cmbRegion.addItem(name)
			self.regionIndexToId[index] = id
			index += 1

		self.cmbRegion.setCurrentIndex(idCmb)

		# cmbSport
		bd = Bbdd()
		data = bd.select("sport", "name")

		self.sportIndexToId = {}
		index, idCmb = 0, 0
		idBd = bd.getValue(self.id, "competition", "sport")
		for i in data:
			id = i[0]
			if id == idBd:
				idCmb = index
			name = i[1]
			self.cmbSport.addItem(name)
			self.sportIndexToId[index] = id
			index += 1

		self.cmbSport.setCurrentIndex(idCmb)

		bd.close()

	def close(self):
			self.mainWindows.setCentralWidget(Competitions(self.mainWindows))

	def cancel(self):
		self.close()

	def accept(self):
		data = []
		data.append(self.txtName.text())
		idRegion = self.regionIndexToId.get(self.cmbRegion.currentIndex())
		data.append(idRegion)
		idSport = self.sportIndexToId.get(self.cmbSport.currentIndex())
		data.append(idSport)



		columns = ["name", "region", "sport"]

		bbdd = Bbdd()
		bbdd.update(columns, data, "competition", "id="+self.id)
		bbdd.close()

		QMessageBox.information(self, _("Updated"), _("Updated competition."))

		self.close()

