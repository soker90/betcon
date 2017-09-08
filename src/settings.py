import sys, os, inspect
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
		file = LibYaml()
		config = file.load()

