import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5 import uic
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from bbdd import Bbdd
from tipsters_month import TipstersMonth
from gettext import gettext as _
import gettext

class NewTipsterMonth(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/new_tipster_month.ui", self)
		gettext.textdomain("betcon")
		gettext.bindtextdomain("betcon", "../lang/mo")
		self.mainWindows = mainWindows
		self.btnAccept.clicked.connect(self.accept)
		self.btnCancel.clicked.connect(self.cancel)
		self.mainWindows.setWindowTitle(_("New Tipster Payment") + " | Betcon v" + mainWindows.version)

		self.initData()
		self.translate()

	def translate(self):
		self.lblMonth.setText(_("Month"))
		self.lblYear.setText(_("Year"))
		self.lblTipster.setText(_("Tipster"))
		self.lblAmount.setText(_("Amount"))

		self.cmbMonth.addItems([_("January"), _("February"), _("March"), _("April"), _("May"), _("June"), _("July"),
		                        _("August"), _("September"), _("October"), _("November"), _("December")])

		self.btnCancel.setText(_("Cancel"))
		self.btnAccept.setText(_("Accept"))

	def initData(self):
		bd = Bbdd()
		data = bd.select("tipster", "name")

		self.tipsterIndexToId = {}
		index = 0
		for i in data:
			id = i[0]
			name = i[1]
			self.cmbTipster.addItem(name)
			self.tipsterIndexToId[index] = id
			index += 1

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
		bbdd.insert(columns, data, "tipster_month")
		bbdd.close()

		QMessageBox.information(self, _("Added"), _("New tipster payment added."))

		self.close()

