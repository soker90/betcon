import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5 import uic
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from bbdd import Bbdd
from banks import Banks
from datetime import datetime
from PyQt5.QtCore import QDate
from gettext import gettext as _
import gettext
from libyaml import LibYaml

class NewBank(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/new_bank.ui", self)
		gettext.textdomain("betcon")
		gettext.bindtextdomain("betcon", "../lang/mo" + mainWindows.lang)
		gettext.bindtextdomain("betcon", "/usr/share/locale" + mainWindows.lang)
		self.mainWindows = mainWindows
		self.btnAccept.clicked.connect(self.accept)
		self.btnCancel.clicked.connect(self.cancel)
		self.mainWindows.setWindowTitle(_("New Movement") + " | Betcon v" + mainWindows.version)

		self.coin = LibYaml().interface["coin"]
		self.initData()
		self.translate()

	def translate(self):

		self.lblDate.setText(_("Date"))
		self.lblBookie.setText(_("Bookie"))
		self.lblType.setText(_("Type"))
		self.lblAccount.setText(_("Account"))
		self.lblAmount.setText(_("Amount"))

		self.cmbAccount.addItems([_("Bank"), "Paypal", "Skrill"])
		self.cmbType.addItems([_("Deposit")  + "(" + self.coin + ")", _("Withdraw") + "(" + self.coin + ")"])

		self.btnCancel.setText(_("Cancel"))
		self.btnAccept.setText(_("Accept"))

	def initData(self):
		sDate = datetime.now().strftime('%Y-%m-%d')
		dDate = QDate.fromString(sDate, "yyyy-MM-dd")
		self.txtDate.setDate(dDate)

		# cmbBookie
		bd = Bbdd()
		data = bd.select("bookie", "name")

		self.bookieIndexToId = {}
		index = 0
		for i in data:
			id = i[0]
			name = i[1]
			self.cmbBookie.addItem(name)
			self.bookieIndexToId[index] = id
			index += 1

		bd.close()

	def close(self):
		self.mainWindows.setCentralWidget(Banks(self.mainWindows))

	def cancel(self):
		self.close()

	def accept(self):
		data = []

		data.append(self.txtDate.text())
		data.append(self.cmbAccount.currentIndex()+1)
		idBookie = self.bookieIndexToId.get(self.cmbBookie.currentIndex())
		data.append(idBookie)
		if self.cmbType.currentIndex() == 1:
			type = "-"
		else:
			type = ""

		money = type+str(self.txtMoney.text())
		data.append(money)

		columns = ["date", "account", "bookie", "money"]

		bbdd = Bbdd()
		bbdd.insert(columns, data, "movement")

		money = float(money) * (-1)
		data = ["'+bank+'" + str(money)]
		columns = ["bank"]

		account = self.cmbAccount.currentIndex()
		bbdd.update(columns, data, "bank", "id="+str(account + 1))
		bbdd.close()

		QMessageBox.information(self, _("Added"), _("Added movement."))
		self.close()

