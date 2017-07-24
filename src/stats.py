import sys
from PyQt5.QtWidgets import QMessageBox, QWidget, QTreeWidgetItem
from PyQt5 import uic
from libstats import LibStats
from datetime import datetime

sys.path.append("./lib")
from bookie import Bookie



class Stats(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		uic.loadUi("../ui/stats.ui", self)
		self.mainWindows = mainWindows
		self.mainWindows.setWindowTitle("Estadisticas | Betcon")

		self.initData()


	def initData(self):
		year = datetime.now().strftime('%Y')
		month = datetime.now().strftime('%m')
		data = LibStats.getMonth(year, month)
		self.txtApostado.setText(str(data[0]))
		self.txtGanancias.setText(str(data[1]))
		self.txtPerdidas.setText(str(data[2]))
		self.txtBeneficio.setText(str(data[3]))
		self.txtPendiente.setText(str(data[4]))
		self.txtYield.setText(str(data[5]))
		self.txtCuota.setText(str(data[6]))
		self.txtApuestas.setText(str(data[7]))
		self.txtAciertos.setText(str(data[8]))
		self.txtFallos.setText(str(data[9]))
		self.txtNulos.setText(str(data[10]))
		self.txtAcierto.setText(str(data[11]))
		self.txtApuestaMedia.setText(str(data[12]))

