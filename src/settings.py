import sys, os, inspect

from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from bbdd import Bbdd
from libyaml import LibYaml
from bets import Bets
from func_aux import str_to_float
from bookie import Bookie
from gettext import gettext as _
import gettext


class Settings(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/settings.ui", self)
		gettext.textdomain("betcon")
		gettext.bindtextdomain("betcon", "../lang/mo")
		self.mainWindows = mainWindows
		mainWindows.diconnectActions()
		self.mainWindows.setWindowTitle(_("Options") + " | Betcon v" + mainWindows.version)
		self.translate()
		self.btnAccept.clicked.connect(self.accept)
		self.btnCancel.clicked.connect(self.cancel)
		self.config = LibYaml()
		self.txtPercentage.setValue(float(self.config.stake["percentage"]))
		self.cmbOne.setCurrentIndex(self.config.stake["type"])
		self.txtStake.setValue(float(self.config.stake["stake"]))
		if self.config.stake["type"] == 0:
			self.txtStake.setEnabled(False)
		self.cmbOne.activated.connect(self.updateOne)
		self.btnCalc.clicked.connect(self.calcBank)


	def translate(self):
		self.lblCalculate.setText(_("Stake 1 calculation"))
		self.lblPercentage.setText(_("Stake 1 percentage"))
		self.lblStake.setText(_("Stake 1"))

		self.cmbOne.addItems([_("Calculated"), _("Fixed")])

		self.btnCalc.setText(_("Calculate"))
		self.btnCancel.setText(_("Cancel"))
		self.btnAccept.setText(_("Accept"))

	def updateOne(self):
		result = self.cmbOne.currentIndex()
		self.txtStake.setEnabled(False) if result == 0 else self.txtStake.setEnabled(True)

	def calcBank(self):
		bd = Bbdd()
		bookies = Bookie.sumAll()
		bonus = Bookie.sumBonus()

		# CC
		cc = bd.select("bank", None, "id=1", "bank")
		cc = cc[0][0]

		# Paypal
		paypal = bd.select("bank", None, "id=2", "bank")
		paypal = paypal[0][0]

		# SKRILL
		skrill = bd.select("bank", None, "id=3", "bank")
		skrill = skrill[0][0]

		total = "{0:.2f}".format(cc + paypal + skrill + bonus + bookies)
		total = float(total) * (self.txtPercentage.value() * 0.01)
		self.txtStake.setValue(float(total))

	def close(self):
		self.mainWindows.enableTools()
		self.mainWindows.setCentralWidget(Bets(self.mainWindows))

	def cancel(self):
		self.close()

	def accept(self):
		self.config.stake["percentage"] = self.txtPercentage.text()[:-1]
		self.config.stake["type"] = self.cmbOne.currentIndex()
		self.config.stake["stake"] = self.txtStake.text()[:-1]
		self.config.save()
		self.close()

