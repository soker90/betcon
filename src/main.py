import inspect
import os
import sys
from os.path import expanduser

directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDialog, QFileDialog
from PyQt5 import uic
from PyQt5.Qt import QIcon
sys.path.append(directory)
from bets import Bets
from new_bet import NewBet
sys.path.append(directory + "/lib")

from regions import Regions
from new_region import NewRegion
from competitions import Competitions
from new_competition import NewCompetition
from sports import Sports
from new_sport import NewSport
from bookies import Bookies
from new_bookie import NewBookie
from markets import Markets
from new_market import NewMarket
from tipsters import Tipsters
from new_tipster import NewTipster
from edit_bet import EditBet
from edit_bookie import EditBookie
from edit_competition import EditCompetition
from edit_tipster import EditTipster
from edit_market import EditMarket
from edit_region import EditRegion
from edit_sport import EditSport
from stats import Stats
from banks import Banks
from bonus import Bonus
from new_bank import NewBank
from stats_tipster import StatsTipster
from stats_bookie import StatsBookie
from stats_market import StatsMarket
from stats_region import StatsRegion
from stats_sport import StatsSport
from stats_stake import StatsStake
from add_money import AddMoney
from new_bonus import NewBonus
from edit_bonus import EditBonus
from new_tipster_month import NewTipsterMonth
from tipsters_month import TipstersMonth
from edit_tipster_month import EditTipsterMonth
from new_conjunta import NewConjunta
from edit_conjunta import EditConjunta
from ods import Ods
from settings import Settings
from gettext import gettext as _
import gettext
from func_aux import openUrl
from libyaml import LibYaml
import platform


class Main(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		uic.loadUi(directory + "/../ui/wmain.ui", self)
		if platform.system() != 'Linux':
			self.lang = "/" + LibYaml().interface["lang"]
		else:
			self.lang = ""
		gettext.textdomain("betcon")
		gettext.bindtextdomain("betcon", "../lang/mo" + self.lang)
		gettext.bindtextdomain("betcon", "/usr/share/locale" + self.lang)
		self.showMaximized()
		self.enableTools()

		archivo = open(directory+"/version.txt")
		self.version = archivo.readline()
		self.setWindowTitle(_("Home") + " | Betcon v" + self.version)
		if os.path.isfile("/usr/share/pixmaps/betcon.png"):
			image = "/usr/share/pixmaps/betcon.png"
		else:
			image = directory + '/../resources/icon.png'
		self.setWindowIcon(QIcon(image))

		self.aInicio.triggered.connect(self.home)
		self.aInicio.setText(_("Home"))
		self.aRegion.triggered.connect(self.regions)
		self.aRegion.setText(_("Regions"))
		self.aCompetition.triggered.connect(self.competitions)
		self.aCompetition.setText(_("Competitions"))
		self.aSport.triggered.connect(self.sports)
		self.aSport.setText(_("Sports"))
		self.aBookie.triggered.connect(self.bookies)
		self.aBookie.setText(_("Bookies"))
		self.aMarket.triggered.connect(self.markets)
		self.aMarket.setText(_("Markets"))
		self.aTipster.triggered.connect(self.tipsters)
		self.aTipster.setText(_("Tipsters"))
		self.aStat.triggered.connect(self.stats)
		self.aStat.setText(_("Stats"))
		self.aBank.triggered.connect(self.banks)
		self.aBank.setText(_("Bank"))
		self.aBonus.triggered.connect(self.bonus)
		self.aBonus.setText(_("Bonus"))
		self.aTipsterMonth.triggered.connect(self.tipstersMonth)
		self.aTipsterMonth.setText(_("Payment history"))

		self.aStatsGeneral.triggered.connect(self.stats)
		self.aStatsGeneral.setText(_("General"))
		self.aStatsTipster.triggered.connect(self.statsTipster)
		self.aStatsTipster.setText(_("Tipsters"))
		self.aStatsBookie.triggered.connect(self.statsBookie)
		self.aStatsBookie.setText(_("Bookies"))
		self.aStatsMarket.triggered.connect(self.statsMarket)
		self.aStatsMarket.setText(_("Markets"))
		self.aStatsRegion.triggered.connect(self.statsRegion)
		self.aStatsRegion.setText(_("Regions"))
		self.aStatsSport.triggered.connect(self.statsSport)
		self.aStatsSport.setText(_("Sports"))
		self.aStatsStake.triggered.connect(self.statsStake)
		self.aStatsStake.setText(_("Stake"))

		self.aAddMoney.triggered.connect(self.addMoney)
		self.aAddMoney.setText(_("Add/Withdraw funds"))
		self.aClose.triggered.connect(self.close)
		self.aClose.setText(_("Close"))
		self.aAbout.triggered.connect(self.about)
		self.aAbout.setText(_("About..."))
		self.aSettings.triggered.connect(self.settings)
		self.aSettings.setText(_("Settings"))
		self.aDonate.triggered.connect(self.donate)
		self.aDonate.setText(_("Donate"))

		self.aNewConjunta.triggered.connect(self.newConjunta)
		self.aNewConjunta.setText(_("New joint purchase"))
		self.aExport.triggered.connect(self.export)
		self.aExport.setText(_("Export"))
		self.aImport.triggered.connect(self.imports)
		self.aImport.setText(_("Import"))

		self.aNew.setText(_("New"))
		self.aEdit.setText(_("Edit"))
		self.aRemove.setText(_("Delete"))

		self.aEditConjunta.setText(_("Edit joint purchase"))
		self.aDeleteConjunta.setText(_("Delete joint purchase"))

		self.menuArchivo.setTitle(_("File"))
		self.menuAyuda.setTitle(_("Help"))

		self.setCentralWidget(Bets(self))



	#ToolPrimary

	def home(self):
		self.setCentralWidget(Bets(self))
		self.enableTools()

	def regions(self):
		self.setCentralWidget(Regions(self))
		self.enableTools()

	def competitions(self):
		self.setCentralWidget(Competitions(self))
		self.enableTools()

	def sports(self):
		self.setCentralWidget(Sports(self))
		self.enableTools()

	def bookies(self):
		self.setCentralWidget(Bookies(self))
		self.enableTools()

	def markets(self):
		self.setCentralWidget(Markets(self))
		self.enableTools()

	def tipsters(self):
		self.setCentralWidget(Tipsters(self))
		self.enableTools("tipster")

	def tipstersMonth(self):
		self.setCentralWidget(TipstersMonth(self))
		self.enableTools("tipster_money")

	def stats(self):
		self.setCentralWidget(Stats(self))
		self.enableTools("stats")

	def banks(self):
		self.setCentralWidget(Banks(self))
		self.enableTools("bank")

	def bonus(self):
		self.setCentralWidget(Bonus(self))
		self.enableTools()

	# ToolSecundary
	# New Buttons

	def newBet(self):
		self.setCentralWidget(NewBet(self))
		self.enableTools()

	def newRegion(self):
		self.setCentralWidget(NewRegion(self))
		self.enableTools()

	def newCompetition(self):
		self.setCentralWidget(NewCompetition(self))
		self.enableTools()

	def newSport(self):
		self.setCentralWidget(NewSport(self))
		self.enableTools()

	def newBookie(self):
		self.setCentralWidget(NewBookie(self))
		self.enableTools()

	def newMarket(self):
		self.setCentralWidget(NewMarket(self))
		self.enableTools()

	def newTipster(self):
		self.setCentralWidget(NewTipster(self))
		self.enableTools("tipster")

	def newTipsterMonth(self):
		self.setCentralWidget(NewTipsterMonth(self))
		self.enableTools("tipster")

	def newBank(self):
		self.setCentralWidget(NewBank(self))
		self.enableTools("bank")

	def newBonus(self):
		self.setCentralWidget(NewBonus(self))
		self.enableTools()

	# Edit Buttons

	def editBet(self, id):
		self.setCentralWidget(EditBet(self, id))
		self.enableTools()

	def editRegion(self, id):
		self.setCentralWidget(EditRegion(self, id))
		self.enableTools()

	def editCompetition(self, id):
		self.setCentralWidget(EditCompetition(self, id))
		self.enableTools()

	def editSport(self, id):
		self.setCentralWidget(EditSport(self, id))
		self.enableTools()

	def editBookie(self, id):
		self.setCentralWidget(EditBookie(self, id))
		self.enableTools()

	def editMarket(self, id):
		self.setCentralWidget(EditMarket(self, id))
		self.enableTools()

	def editTipster(self, id):
		self.setCentralWidget(EditTipster(self, id))
		self.enableTools()

	def editTipsterMonth(self, id):
		self.setCentralWidget(EditTipsterMonth(self, id))
		self.enableTools("tipster")

	def editBonus(self, id):
		self.setCentralWidget(EditBonus(self, id))
		self.enableTools()

	# Stats

	def statsTipster(self):
		self.setCentralWidget(StatsTipster(self))

	def statsBookie(self):
		self.setCentralWidget(StatsBookie(self))

	def statsMarket(self):
		self.setCentralWidget(StatsMarket(self))

	def statsRegion(self):
		self.setCentralWidget(StatsRegion(self))

	def statsSport(self):
		self.setCentralWidget(StatsSport(self))

	def statsStake(self):
		self.setCentralWidget(StatsStake(self))

	# Bank

	def addMoney(self):
		self.setCentralWidget(AddMoney(self))

	# Conjunta
	def newConjunta(self):
		self.setCentralWidget(NewConjunta(self))

	def editConjunta(self, id):
		self.setCentralWidget(EditConjunta(self, id))
		self.enableActionConjunta(False)

	def settings(self):
		self.setCentralWidget(Settings(self))
		self.enableTools("settings")

	#Auxiliary Functions

	def enableTools(self, type=None):
		self.toolBank.setVisible(False)
		self.toolTipster.setVisible(False)
		self.toolConjunta.setVisible(False)
		if type is "stats":
			self.toolSecondary.setVisible(False)
			self.toolStat.setVisible(True)
		elif type is "settings":
			self.toolSecondary.setVisible(False)
		else:
			self.toolSecondary.setVisible(True)
			self.toolStat.setVisible(False)
			self.aEdit.setEnabled(False)
			self.aRemove.setEnabled(False)
			if type is "bank":
				self.toolBank.setVisible(True)
			if type is "tipster":
				self.toolTipster.setVisible(True)
			if type is "tipster_money":
				self.toolTipster.setVisible(True)
				self.toolConjunta.setVisible(True)

	def enableActions(self, edit=True):
		if edit:
			self.aEdit.setEnabled(True)
		self.aRemove.setEnabled(True)

	def enableActionConjunta(self, enable):
		self.aEditConjunta.setEnabled(enable)
		self.aDeleteConjunta.setEnabled(enable)

	def diconnectActions(self):
		try:
			self.aNew.triggered.disconnect()
		except:
			pass
		try:
			self.aEdit.triggered.disconnect()
		except:
			pass
		try:
			self.aRemove.triggered.disconnect()
		except:
			pass


	#Events

	def closeEvent(self, event):
		resultado = QMessageBox.question(self, _("Quit"), _("Are you sure you want to exit the application?"),
										 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if resultado == QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()

	# Import/Export
	def export(self):
		file = QFileDialog.getSaveFileName(None, _("Export data"), expanduser("~/") + "betcon.ods", "*.ods")
		if file[0] != '':
			ods = Ods(file[0])
			ods.export()
			QMessageBox.information(self, _("Exported"), _("Exported data"), QMessageBox.Ok)

	def imports(self):
		file = QFileDialog.getOpenFileName(None, _("Import data"), expanduser("~/"), "*.ods")
		if file[0] != '':
			ods = Ods(file[0])
			err = ods.imports()
			if err:
				QMessageBox.warning(self, "Error", err, QMessageBox.Ok)
			else:
				QMessageBox.information(self, _("Imported"), _("Imported data"), QMessageBox.Ok)
		self.setCentralWidget(Bets(self))


	def about(self):
		about = About()
		about.exec_()

	def donate(self):
		openUrl("https://www.paypal.me/eduparra")


class About(QDialog):
	def __init__(self):
		QDialog.__init__(self)
		uic.loadUi(directory + "/../ui/about.ui", self)
		archivo = open(directory + "/version.txt")
		version = archivo.readline()
		self.setWindowTitle(_("About"))
		self.txtText.setHtml("<p style='text-align: center;'><br>Betcon v" + version + "<p/>" \
		                     "<p style='text-align: center;'>Web: http://betcon.eduardoparra.es/<p/>" \
		                     "<p style='text-align: center;'>" + _("Created by") + " Eduardo Parra Mazuecos<p/>" \
		                     "<p style='text-align: center;'>" + _("Contact") + ": eduparra90@gmail.com</p>" \
			                 "<p style='text-align: center;'>" + _("License") +" GPLv3<p/>" \
		                     "<p style='text-align: center;'>" + _("Translated by:") + "<p/>" \
			                 "<p style='text-align: center;'>" + "English: Eduardo Parra Mazuecos. <p/>" \
		                     "<p style='text-align: center;'>" + "Spanish: Eduardo Parra Mazuecos. <p/>" \
		                     "<p style='text-align: center;'>" + "Brazilian Portuguese: Rodrigo Henrique. <p/>" \
		                     "<p style='text-align: center;'>" + "German: Franz Lewin Wagner, Rokar. <p/>" \
				     "<p style='text-align: center;'>" + "Kurdish: Rokar. <p/>" \
		                     "<p style='text-align: center;'>" + "Turkish: zeugma. <p/>" )


