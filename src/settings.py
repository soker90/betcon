import sys, os, inspect

from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from libyaml import LibYaml
from bets import Bets
from func_aux import str_to_float


class Settings(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/settings.ui", self)
		self.mainWindows = mainWindows
		mainWindows.diconnectActions()
		self.mainWindows.setWindowTitle("Opciones | Betcon v" + mainWindows.version)
		self.btnAccept.clicked.connect(self.accept)
		self.btnCancel.clicked.connect(self.cancel)
		self.config = LibYaml()
		self.txtPercentage.setValue(self.config.stake["percentage"])
		self.cmbOne.setCurrentIndex(self.config.stake["type"])
		self.txtStake.setValue(self.config.stake["stake"])
		if self.config.stake["type"] == 0:
			self.txtStake.setEnabled(False)
		self.cmbOne.activated.connect(self.updateOne)

	def updateOne(self):
		result = self.cmbOne.currentIndex()
		self.txtStake.setEnabled(False) if result == 0 else self.txtStake.setEnabled(True)

	def close(self):
		self.mainWindows.setCentralWidget(Bets(self.mainWindows))

	def cancel(self):
		self.close()

	def accept(self):
		self.config.stake["percentage"] = str_to_float(self.txtPercentage.text()[:-1])
		self.config.stake["type"] = self.cmbOne.currentIndex()
		self.config.stake["stake"] = str_to_float(self.txtStake.text()[:-1])
		self.config.save()
		self.close()

