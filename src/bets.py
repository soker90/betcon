import sys
import os
from lib.paths import get_base_dir
import inspect
from PySide6.QtWidgets import QWidget, QAbstractItemView, QMessageBox
from PySide6.QtCore import QEvent
from uiloader import loadUi
directory = get_base_dir()
sys.path.append(directory + "/lib")
from bbdd import Bbdd
from func_aux import numberToResult, monthToNumber
from libyaml import LibYaml
from os.path import expanduser
from libstats import LibStats
from table_model import BetconTableModel, paint_row_items, make_icon_item, make_item, BetconItemDelegate



class Bets(QWidget):
	def __init__(self, mainWindows):
		QWidget.__init__(self)
		loadUi(directory + "/../ui/bets.ui", self)
		self.mainWindows = mainWindows
		mainWindows.diconnectActions()
		mainWindows.aNew.triggered.connect(mainWindows.newBet)
		self.mainWindows.setWindowTitle(_("Home") + " | Betcon v" + mainWindows.version)
		header = [" ", "index", _("Date"), _("Sport"), _("Competition"), _("Region"), _("Local Team"), _("Away Team"),
		          _("Pick"), _("Bookie"), _("Market"), _("Tipster"), _("Stake"), _("Stake 1"), _("Bet"), _("Quota"),
		          _("Result"), _("Profit")]
		self.lblYear.setText(_("Year"))
		self.lblMonth.setText(_("Month"))

		self.coin = LibYaml().interface["coin"]

		self.model = BetconTableModel()
		self.model.setup(header, hidden_col=1)
		self.treeMain.setModel(self.model)
		self.treeMain.setAlternatingRowColors(False)
		self._delegate = BetconItemDelegate(self.treeMain)
		self.treeMain.setItemDelegate(self._delegate)
		self.treeMain.setMouseTracking(True)
		self.treeMain.viewport().setMouseTracking(True)
		self.treeMain.viewport().installEventFilter(self)
		self.treeMain.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
		self.treeMain.horizontalHeader().setStretchLastSection(True)
		self.treeMain.verticalHeader().setVisible(False)
		self.treeMain.verticalHeader().setDefaultSectionSize(24)
		self.treeMain.setSortingEnabled(True)

		font = self.treeMain.font()
		font.setPointSizeF(font.pointSizeF() + 1)
		font.setBold(True)
		self.treeMain.setFont(font)
		self.treeMain.verticalHeader().setDefaultSectionSize(28)

		try:
			self.initData()
		except Exception as e:
			print(f"No hay datos: {e}")
		self.treeMain.selectionModel().selectionChanged.connect(self.changeItem)
		self.mainWindows.aEdit.triggered.connect(self.editItem)
		self.mainWindows.aRemove.triggered.connect(self.deleteItem)
		self.cmbYear.activated.connect(self.updateMonths)
		self.cmbMonth.activated.connect(self.initTree)

		self.itemSelected = -1
		self.treeMain.setColumnHidden(1, True)



	def eventFilter(self, obj, event):
		if obj is self.treeMain.viewport():
			if event.type() == QEvent.Type.MouseMove:
				index = self.treeMain.indexAt(event.pos())
				row = index.row() if index.isValid() else -1
				if row != self._delegate._hovered_row:
					self._delegate.set_hovered_row(row)
					self.treeMain.viewport().update()
			elif event.type() == QEvent.Type.Leave:
				self._delegate.set_hovered_row(-1)
				self.treeMain.viewport().update()
		return super().eventFilter(obj, event)

	def initData(self):
		self.years, self.months = LibStats.getYears()
		self.cmbYear.addItems(self.years.keys())
		self.updateMonths()

	def updateMonths(self):
		year = self.cmbYear.currentText()
		self.cmbMonth.clear()
		self.cmbMonth.addItems(self.getMonths(year))
		self.initTree()


	def initTree(self):
		year = self.cmbYear.currentText()
		month = self.cmbMonth.currentText()
		month = monthToNumber(month)
		self.model.removeRows(0, self.model.rowCount())
		bd = Bbdd()
		query = (
			"SELECT b.id, b.date, b.sport, b.competition, b.region, b.player1, b.player2, "
			"b.pick, b.bookie, b.market, b.tipster, b.stake, b.one, b.result, b.profit, b.bet, b.quota, "
			"c.name, r.name, m.name, t.name, s.name, bk.name "
			"FROM bet b "
			"LEFT JOIN competition c ON b.competition = c.id "
			"LEFT JOIN region r ON b.region = r.id "
			"LEFT JOIN market m ON b.market = m.id "
			"LEFT JOIN tipster t ON b.tipster = t.id "
			"LEFT JOIN sport s ON b.sport = s.id "
			"LEFT JOIN bookie bk ON b.bookie = bk.id "
			"WHERE b.date LIKE ? ORDER BY b.date DESC"
		)
		data = bd.executeQuery(query, (f"{year}-{month}%",))

		for index, i in enumerate(data, start=1):
			sport_id    = str(i[2])
			bookie_id   = str(i[8])
			competition = str(i[17]) if i[17] else ""
			region      = str(i[18]) if i[18] else ""
			market      = str(i[19]) if i[19] else ""
			tipster     = str(i[20]) if i[20] else ""
			sport_name  = str(i[21]) if i[21] else ""
			bookie_name = str(i[22]) if i[22] else ""
			profit      = i[14]

			sport_icon = None
			for path in [
				expanduser("~") + "/.betcon/resources/sports/" + sport_id + ".png",
				directory + "/../resources/sports/" + sport_id + ".png",
			]:
				if os.path.isfile(path):
					sport_icon = path
					break

			bookie_icon = None
			for path in [
				expanduser("~") + "/.betcon/resources/bookies/" + bookie_id + ".png",
				directory + "/../resources/bookies/" + bookie_id + ".png",
			]:
				if os.path.isfile(path):
					bookie_icon = path
					break

			row = [
				make_item(str(index)),
				make_item(str(i[0])),
				make_item(str(i[1])[:-3]),
				make_icon_item(sport_icon, sport_name),
				make_item(competition),
				make_item(region),
				make_item(str(i[5])),
				make_item(str(i[6])),
				make_item(str(i[7])),
				make_icon_item(bookie_icon, bookie_name),
				make_item(market),
				make_item(tipster),
				make_item(str(i[11])),
				make_item(str(i[12]) + self.coin),
				make_item(str(i[15]) + self.coin),
				make_item(str(i[16])),
				make_item(numberToResult(i[13])),
				make_item(str(profit) + self.coin),
			]
			paint_row_items(row, float(profit), i[13])
			self.model.appendRow(row)

		self.treeMain.resizeColumnsToContents()
		# Sport (col 3) and Bookie (col 9) images are 100px wide
		self.treeMain.setColumnWidth(3, 104)
		self.treeMain.setColumnWidth(9, 104)
		bd.close()

	def changeItem(self):
		indexes = self.treeMain.selectionModel().selectedRows()
		if not indexes:
			return
		row = indexes[0].row()
		self.itemSelected = self.model.get_id(row)
		self.mainWindows.enableActions()

	def editItem(self):
		self.mainWindows.editBet(self.itemSelected)

	def deleteItem(self):
		resultado = QMessageBox.question(self, _("Remove"), _("Are you sure you want to eliminate it?"),
										 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if resultado == QMessageBox.Yes:
			bd = Bbdd()
			bd.delete("bet", self.itemSelected)
			bd.deleteWhere("combined", "bet=?", (self.itemSelected,))
			self.mainWindows.setCentralWidget(Bets(self.mainWindows))
			self.mainWindows.enableTools()

	def getMonths(self, year):
		sMonths = []
		for i in self.years[year]:
			sMonths.append(self.months[i])
		return sMonths





