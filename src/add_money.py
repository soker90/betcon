import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5 import uic
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from banks import Banks
from bbdd import Bbdd
from gettext import gettext as _
import gettext


class AddMoney(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/add_money.ui", self)
		gettext.textdomain("betcon")
		gettext.bindtextdomain("betcon", "../lang/mo")
		gettext.bindtextdomain("betcon", "/usr/share/locale")
		self.mainWindows = mainWindows
		mainWindows.aNew.triggered.connect(mainWindows.newBank)
		self.mainWindows.setWindowTitle(_("Add funds") + " | Betcon v" + mainWindows.version)
		self.btnAccept.clicked.connect(self.accept)
		self.btnCancel.clicked.connect(self.cancel)
		#self.txtMoney.returnPressed.connect(self.btnAccept.click)
		self.translate()

	def translate(self):

		self.lblAccount.setText(_("Account"))
		self.lblType.setText(_("Type"))
		self.lblAmount.setText(_("Amount"))

		self.cmbAccount.addItems([_("Bank"), "Paypal", "Skrill"])
		self.cmbType.addItems([_("Deposit"), _("Withdraw")])

		self.btnCancel.setText(_("Cancel"))
		self.btnAccept.setText(_("Accept"))

	def close(self):
			self.mainWindows.setCentralWidget(Banks(self.mainWindows))

	def cancel(self):
		self.close()

	def accept(self):
		type = self.cmbType.currentIndex()
		if type == 0:
			type="+"
		else:
			type="-"

		data = ["'+bank"+type+"'"+str(self.txtMoney.text())]
		columns = ["bank"]

		account = self.cmbAccount.currentIndex()

		bbdd = Bbdd()
		bbdd.update(columns, data, "bank", "id="+str(account+1))
		bbdd.close()

		QMessageBox.information(self, _("Added"), _("Added funds."))

		self.close()
