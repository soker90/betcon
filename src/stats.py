import sys
import os
import inspect
import pyqtgraph as pg
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtGui import QPalette
from uiloader import loadUi
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from libstats import LibStats
from func_aux import key_from_value, monthToNumber
from gettext import gettext as _
import gettext
from libyaml import LibYaml


class Stats(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		loadUi(directory + "/../ui/stats.ui", self)
		gettext.textdomain("betcon")
		local_mo = os.path.normpath(directory + "/../lang/mo" + mainWindows.lang)
		if os.path.isdir(local_mo):
			gettext.bindtextdomain("betcon", local_mo)
		else:
			gettext.bindtextdomain("betcon", "/usr/share/locale" + mainWindows.lang)
		self._gt = gettext.translation(
			"betcon",
			localedir=local_mo if os.path.isdir(local_mo) else "/usr/share/locale",
			fallback=True,
		)
		self.mainWindows = mainWindows
		self.mainWindows.setWindowTitle(_("Stats") + " | Betcon v" + mainWindows.version)

		self.coin = LibYaml().interface["coin"]
		self.translate()

		self.initData()
		self.cmbYear.activated.connect(self.updateMonths)
		self.cmbMonth.activated.connect(self.updateDays)
		self.cmbDay.activated.connect(self.updateStats)
		self.initChart()
		self.cmbYear.activated.connect(self.updateChart)

	def translate(self):
		self.lblDay.setText(_("Day"))
		self.grpBalance.setTitle(_("Balance of the bets of the month"))
		self.grpBets.setTitle(_("Bets"))
		self.lblBet.setText(_("Money Bet"))
		self.lblWinnings.setText(_("Winnings"))
		self.lblLosses.setText(_("Losses"))
		self.lblProfits.setText(_("Profits"))
		self.lblPending.setText(_("Pending"))
		self.lblYield.setText(_("Yield"))
		self.lblQuota.setText(_("Average Quota"))
		self.lblBets.setText(_("Bets"))
		self.lblWon.setText(_("Won"))
		self.lblLost.setText(_("Lost"))
		self.lblNull.setText(_("Null"))
		self.lblSuccess.setText(_("Success"))
		self.lblAverageBet.setText(_("Average Bet"))


	def initData(self):
		self.years, self.months = LibStats.getYears()
		self.cmbYear.addItems(self.years.keys())
		self.cmbDay.addItem("")

		try:
			firstKey = next(iter(self.years))
			self.cmbMonth.addItems(self.getMonths(firstKey))

			self.updateMonths()
			self.updateDays()
		except Exception:
			self.setEnabled(False)

	def updateMonths(self):
		year = self.cmbYear.currentText()
		self.cmbMonth.clear()
		self.cmbMonth.addItems(self.getMonths(year))

		try:
			self.cmbMonth.setCurrentIndex(1)
		except Exception:
			self.cmbMonth.setCurrentIndex(0)
		self.updateDays()

	def updateDays(self):
		year = self.cmbYear.currentText()
		month = self.cmbMonth.currentText()
		self.cmbDay.clear()
		if month != "" and month is not None:
			try:
				month = monthToNumber(month)

				self.cmbDay.addItem("")
				self.cmbDay.addItems(LibStats.getDaysOfMonth(year, month))
			except Exception:
				pass

		self.updateStats()

	def updateStats(self):
		year = self.cmbYear.currentText()
		sMonth = self.cmbMonth.currentText()
		if sMonth != "" and sMonth is not None:
			month = key_from_value(self.months, sMonth)
			day = self.cmbDay.currentText()
		else:
			month = ""
			day = ""

		try:
			data = LibStats.getMonth(year, month, day)
		except Exception:
			return
		self.txtApostado.setText(str(data[0]) + self.coin)
		self.txtGanancias.setText(str(data[1]) + self.coin)
		self.txtPerdidas.setText(str(data[2]) + self.coin)
		self.txtBeneficio.setText(str(data[3]) + self.coin)
		self.txtPendiente.setText(str(data[4]) + self.coin)
		self.txtYield.setText(str(data[5]))
		self.txtCuota.setText(str(data[6]))
		self.txtApuestas.setText(str(data[7]))
		self.txtAciertos.setText(str(data[8]))
		self.txtFallos.setText(str(data[9]))
		self.txtNulos.setText(str(data[10]))
		self.txtAcierto.setText(str(data[11]))
		self.txtApuestaMedia.setText(str(data[12]) + self.coin)


	def getMonths(self, year):
		sMonths = [""]
		for i in self.years[year]:
			sMonths.append(self.months[i])
		return sMonths

	@staticmethod
	def _chart_colors():
		is_dark = QApplication.instance().palette().color(QPalette.ColorRole.Window).lightnessF() < 0.5
		return {
			'bg':   '#1e1e2e' if is_dark else '#ffffff',
			'fg':   '#cdd6f4' if is_dark else '#1a1a2e',
			'pos':  '#a6e3a1',
			'neg':  '#f38ba8',
		}

	def initChart(self):
		colors = self._chart_colors()
		bg, fg = colors['bg'], colors['fg']

		# Remove the vertical spacer so the chart can expand
		layout = self.layout()
		for i in range(layout.count() - 1, -1, -1):
			item = layout.itemAt(i)
			if item and item.spacerItem():
				layout.removeItem(item)
				break

		self.chartWidget = pg.PlotWidget()
		self.chartWidget.setBackground(bg)
		self.chartWidget.setMinimumHeight(200)
		for axis_name in ('left', 'bottom'):
			ax = self.chartWidget.getAxis(axis_name)
			ax.setPen(pg.mkPen(fg))
			ax.setTextPen(pg.mkPen(fg))

		layout.addWidget(self.chartWidget)
		self.updateChart()

	def updateChart(self):
		colors = self._chart_colors()
		fg = colors['fg']

		year = self.cmbYear.currentText()
		if not year:
			return

		labels, profits = LibStats.getMonthlyProfitsByYear(year)
		self.chartWidget.clear()
		if not labels:
			return

		x = list(range(len(labels)))
		for xi, yi in zip(x, profits):
			color = '#a6e3a1' if yi >= 0 else '#f38ba8'
			bar = pg.BarGraphItem(x=[xi], height=[yi], width=0.6, brush=color, pen=pg.mkPen(None))
			self.chartWidget.addItem(bar)

		bottom = self.chartWidget.getAxis('bottom')
		bottom.setTicks([[(i, lbl[:3]) for i, lbl in enumerate(labels)]])
		self.chartWidget.addLine(y=0, pen=pg.mkPen('gray', width=1))
		self.chartWidget.setTitle(self._gt.gettext('Monthly profit') + f' · {year}', color=fg)

