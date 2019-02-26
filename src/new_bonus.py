import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget, QComboBox
from PyQt5 import uic
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from bbdd import Bbdd
from bonus import Bonus
from datetime import datetime
from PyQt5.QtCore import QDate
from gettext import gettext as _
import gettext

class NewBonus(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		uic.loadUi(directory + "/../ui/new_bonus.ui", self)
		gettext.textdomain("betcon")
		gettext.bindtextdomain("betcon", "../lang/mo" + mainWindows.lang)
		gettext.bindtextdomain("betcon", "/usr/share/locale" + mainWindows.lang)
		self.mainWindows = mainWindows
		self.btnAccept.clicked.connect(self.accept)
		self.btnCancel.clicked.connect(self.cancel)
		self.mainWindows.setWindowTitle(_("New Bonus") + " | Betcon v" + mainWindows.version)
		self.initData()
		self.translate()

	def translate(self):

		self.lblDate.setText(_("Date"))
		self.lblBookie.setText(_("Bookie"))
		self.lblAmount.setText(_("Amount"))

		self.chkFree.setText(_("Freed"))

		self.btnCancel.setText(_("Cancel"))
		self.btnAccept.setText(_("Accept"))

	def initData(self):
		# date
		sDate = datetime.now().strftime('%Y-%m-%d')
		date = QDate.fromString(sDate, "yyyy-MM-dd")
		self.txtDate.setDate(date)

		bd = Bbdd()

		# cmbBookie
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
			self.mainWindows.setCentralWidget(Bonus(self.mainWindows))

	def cancel(self):
		self.close()

	def accept(self):
		data = []

		bbdd = Bbdd()

		# dtDate
		data.append(self.txtDate.date().toPyDate())

		# cmbBookie
		idBookie = self.bookieIndexToId.get(self.cmbBookie.currentIndex())
		data.append(idBookie)

		data.append(str(self.txtMoney.text()))

		free = self.chkFree.isChecked()
		data.append(str(bool(free)))

		columns = ["date", "bookie", "money", "free"]

		bbdd.insert(columns, data, "bonus")

		QMessageBox.information(self, _("Added"), _("New bonus added."))

		self.close()

