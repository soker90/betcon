import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5 import uic

from new_tipster_month import NewTipsterMonth

directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from bbdd import Bbdd
from tipsters_month import TipstersMonth
from gettext import gettext as _
import gettext

class EditTipsterMonth(QWidget):
	def __init__(self, mainWindows, id):
		QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/new_tipster_month.ui", self)
		gettext.textdomain("betcon")
		gettext.bindtextdomain("betcon", "../lang/mo")
		self.mainWindows = mainWindows
		self.btnAccept.clicked.connect(self.accept)
		self.btnCancel.clicked.connect(self.cancel)
		self.mainWindows.setWindowTitle(_("New Payment Tipster") + " | Betcon v" + mainWindows.version)

		self.id = id
		NewTipsterMonth.translate(self)
		self.initData()



	def initData(self):
		bd = Bbdd()

		data = bd.select("tipster_month", None, "id=" + str(self.id))[0]
		dataCmb = bd.select("tipster", "name")

		self.tipsterIndexToId = {}
		index, idCmb = 0, 0
		idBd = data[3]
		for i in dataCmb:
			id = i[0]
			if id == idBd:
				idCmb = index
			name = i[1]
			self.cmbTipster.addItem(name)
			self.tipsterIndexToId[index] = id
			index += 1

		self.cmbTipster.setCurrentIndex(idCmb)

		self.txtYear.setValue(data[2])
		self.cmbMonth.setCurrentIndex(data[1])
		self.txtMoney.setValue(data[4])

		bd.close()

	def close(self):
			self.mainWindows.setCentralWidget(TipstersMonth(self.mainWindows))
			#self.mainWindows.aApuesta.setEnabled(True)

	def cancel(self):
		self.close()

	def accept(self):
		idTipster = self.tipsterIndexToId.get(self.cmbTipster.currentIndex())
		print(idTipster)
		money = str(self.txtMoney.text())
		data = [self.cmbMonth.currentIndex(), self.txtYear.text(), idTipster, money]
		columns = ["month", "year", "tipster", "money"]

		bbdd = Bbdd()
		bbdd.update(columns, data, "tipster_month")
		bbdd.close()

		QMessageBox.information(self, _("Updated"), _("Added tipster payment."))

		self.close()

