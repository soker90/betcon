import sys, os, inspect
from builtins import print

from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from libyaml import LibYaml

class Settings(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/settings.ui", self)
		self.mainWindows = mainWindows
		mainWindows.diconnectActions()
		self.mainWindows.setWindowTitle("Opciones | Betcon v" + mainWindows.version)
		config = LibYaml()
		self.txtPorcentage.setValue(config.stake["porcentage"])
		self.cmbOne.setCurrentIndex(config.stake["type"])
		self.txtStake.setValue(config.stake["stake"])
		if config.stake["type"] != 2:
			self.txtStake.setEnabled(False)

