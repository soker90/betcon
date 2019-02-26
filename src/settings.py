import sys, os, inspect

from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from bbdd import Bbdd
from libyaml import LibYaml
from bets import Bets
from bookie import Bookie
from gettext import gettext as _
import gettext


class Settings(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/settings.ui", self)
		gettext.textdomain("betcon")
		gettext.bindtextdomain("betcon", "../lang/mo" + mainWindows.lang)
		gettext.bindtextdomain("betcon", "/usr/share/locale" + mainWindows.lang)
		self.mainWindows = mainWindows
		mainWindows.diconnectActions()
		self.mainWindows.setWindowTitle(_("Options") + " | Betcon v" + mainWindows.version)

		self.translate()
		self.btnAccept.clicked.connect(self.accept)
		self.btnCancel.clicked.connect(self.cancel)

		# TODO Al cargar el formulario debe actualiza el combobox con el valor del yml
		self.cmbLanguage.addItem("Deutsch", "de")
		self.cmbLanguage.addItem("English", "en")
		self.cmbLanguage.addItem("Español", "es")
		self.cmbLanguage.addItem("Kurdî", "ki")
		self.cmbLanguage.addItem("Português do Brasil", "pt_BR")
		self.cmbLanguage.addItem("Türk", "tr")

		self.config = LibYaml()
		self.txtPercentage.setValue(float(self.config.stake["percentage"]))
		self.cmbOne.setCurrentIndex(self.config.stake["type"])
		self.txtStake.setValue(float(self.config.stake["stake"]))
		if self.config.stake["type"] == 0:
			self.txtStake.setEnabled(False)

		self.cmbOne.activated.connect(self.updateOne)
		self.btnCalc.clicked.connect(self.calcBank)

		self.txtCoin.setText(self.config.interface["coin"])
		if self.config.interface['bookieCountry'] == 'Y':
			self.chkCountryYes.setChecked(True)
		else:
			self.chkCountryNo.setChecked(True)


	def translate(self):
		self.lblSetStake.setText(_("Stake"))
		self.lblCalculate.setText(_("Stake 1 calculation"))
		self.lblPercentage.setText(_("Stake 1 percentage"))
		self.lblStake.setText(_("Stake 1"))

		self.cmbOne.addItems([_("Calculated"), _("Fixed")])

		self.lblInterface.setText(_("Interface"))
		self.lblCoin.setText(_("Coin"))
		self.lblCountry.setText(_("Show countries of the bookies"))
		self.chkCountryYes.setText(_("Yes"))
		self.chkCountryNo.setText(_("No"))

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
		percentage = self.txtPercentage.text()[:-1]
		self.config.stake["percentage"] = float(percentage)

		self.config.stake["type"] = self.cmbOne.currentIndex()

		stake = self.txtStake.text()[:-1]
		self.config.stake["stake"] = float(stake)
		self.config.interface['coin'] = self.txtCoin.text()
		self.config.interface['bookieCountry'] = 'Y' if self.chkCountryYes.isChecked() else 'N'
		self.config.interface['lang'] = self.cmbLanguage.itemData(self.cmbLanguage.currentIndex())
		self.config.save()
		self.close()

