import sys
import os
import inspect
import pyqtgraph as pg
from PySide6.QtWidgets import QMessageBox, QWidget, QTreeWidgetItem, QApplication
from PySide6.QtGui import QPalette
from uiloader import loadUi
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from bbdd import Bbdd
from bookie import Bookie
from libstats import LibStats
from datetime import datetime, date
from libyaml import LibYaml



class Banks(QWidget):
    def __init__(self, mainWindows):
        QWidget.__init__(self)
        loadUi(directory + "/../ui/banks.ui", self)
        self.mainWindows = mainWindows
        mainWindows.diconnectActions()
        mainWindows.aNew.triggered.connect(mainWindows.newBank)
        self.mainWindows.setWindowTitle("Bank | Betcon v" + mainWindows.version)
        self.treeMovement.itemSelectionChanged.connect(self.changeItem)

        self.coin = LibYaml().interface["coin"]

        self.initData()
        self.initTree()
        self.treeMovement.header().hideSection(1)
        self.mainWindows.aRemove.triggered.connect(self.deleteItem)

        self.itemSelected = -1
        self.translate()
        self.initChart()

    def initChart(self):
        is_dark = QApplication.instance().palette().color(QPalette.ColorRole.Window).lightnessF() < 0.5
        bg = '#1e1e2e' if is_dark else '#ffffff'
        fg = '#cdd6f4' if is_dark else '#1a1a2e'
        line_color = '#89b4fa' if is_dark else '#0078d4'

        date_axis = pg.DateAxisItem(orientation='bottom')
        self.chartWidget = pg.PlotWidget(axisItems={'bottom': date_axis})
        self.chartWidget.setBackground(bg)
        self.chartWidget.setMinimumHeight(200)
        for axis_name in ('left', 'bottom'):
            ax = self.chartWidget.getAxis(axis_name)
            ax.setPen(pg.mkPen(fg))
            ax.setTextPen(pg.mkPen(fg))

        dates, profits = LibStats.getBankEvolution()
        if dates:
            timestamps = []
            for d in dates:
                try:
                    ts = datetime.strptime(d[:10], "%Y-%m-%d").timestamp()
                except ValueError:
                    ts = 0.0
                timestamps.append(ts)
            self.chartWidget.plot(timestamps, profits, pen=pg.mkPen(line_color, width=2))
            self.chartWidget.addLine(y=0, pen=pg.mkPen('gray', width=1))

            # Acotar el rango X entre la primera y última fecha con datos
            x_min = timestamps[0]
            x_max = timestamps[-1]
            padding = (x_max - x_min) * 0.02 or 86400  # al menos 1 día de margen
            self.chartWidget.setLimits(xMin=x_min - padding, xMax=x_max + padding)

            # Mostrar de primeras los últimos 90 días (o todo si hay menos)
            view_start = max(x_min, x_max - 90 * 86400)
            self.chartWidget.setXRange(view_start, x_max + padding, padding=0)

        self.chartWidget.setTitle(_('Bank evolution'), color=fg)
        self.layout().insertWidget(1, self.chartWidget)

    def translate(self):

        self.lblDeposits.setText(_("Deposits"))
        self.lblWithdrawals.setText(_("Withdrawals"))
        self.lblTipsters.setText(_("Tipsters"))
        self.lblProfits.setText(_("Profits"))
        self.lblYield.setText(_("Yield"))
        self.lblBookies.setText(_("Bookies"))
        self.lblBank.setText(_("Bank"))
        self.lblTotal.setText(_("Total"))

        self.lblBookiesLong.setText(_("In bookies"))
        self.lblMovements.setText(_("Movements"))

        header = [_("Bookie"), _("Amount")]

        self.treeBookie.setHeaderLabels(header)

        header = [_("Date"), "index",  _("Bookie"), _("Type"), _("Account"), _("Amount")]

        self.treeMovement.setHeaderLabels(header)


    def initData(self):
        self.txtDeposit.setText("{0:.2f}".format(Bookie.sumAll("money>0")) + self.coin)
        self.txtTakeOut.setText("{0:.2f}".format(Bookie.sumAll("money<0"))  + self.coin)
        bookies = Bookie.sumAll()
        bonus = Bookie.sumBonus()
        self.txtBonus.setText("{0:.2f}".format(bonus)  + self.coin)
        self.txtBookie.setText("{0:.2f}".format(bookies + bonus)  + self.coin)

        bd = Bbdd()

        tipsters = bd.sum("tipster_month", "money")
        conjuntas = bd.sum("conjunta", "money")
        self.txtTipster.setText("-" + str(tipsters + conjuntas)  + self.coin)
        profits = bd.sum("bet", "profit") + bonus
        self.txtProfit.setText("{0:.2f}".format(profits - tipsters - conjuntas)  + self.coin)
        bets = bd.sum("bet", "bet")
        try:
            yields = "{0:.2f}%".format((profits/bets)*100)
        except ZeroDivisionError:
            yields = "0.0%"
        self.txtYield.setText(yields)

        # CC
        cc = bd.select("bank", None, "id=1", "bank")
        cc = cc[0][0]
        self.txtCc.setText("{0:.2f}".format(cc)  + self.coin)

        # Paypal
        paypal = bd.select("bank", None, "id=2", "bank")
        paypal = paypal[0][0]
        self.txtPaypal.setText("{0:.2f}".format(paypal)  + self.coin)

        # SKRILL
        skrill = bd.select("bank", None, "id=3", "bank")
        skrill = skrill[0][0]
        self.txtSkrill.setText("{0:.2f}".format(skrill)  + self.coin)

        total = "{0:.2f}".format(cc+paypal+skrill+bonus+bookies)
        self.txtTotal.setText(total  + self.coin)

    def initTree(self):

        self.treeBookie.clear()
        data = Bookie.selectAll()

        items = []
        for i in data:
            bank = Bookie.sumAll("bookie=?", (i.id,))
            bank = 0.0 if bank is None else bank
            bonus = Bookie.sumBonus(bookie_id=i.id)
            bonus = 0.0 if bonus is None else bonus
            bank += bonus
            if 0.01 > bank > -0.01:
                continue
            item = QTreeWidgetItem([i.name, "{0:.2f}".format(bank) + self.coin])
            items.append(item)

        self.treeBookie.addTopLevelItems(items)

        self.treeMovement.clear()

        bd = Bbdd()
        data = bd.select("movement", "date DESC")

        items = []
        for i in data:
            id = i[0]
            try:
                sDate = datetime.strptime(i[1], "%d/%m/%y")
            except ValueError:
                sDate = datetime.strptime(i[1], "%d/%m/%Y")  # Fix for Windows
            sDate = date.strftime(sDate, "%Y/%m/%d")
            account = i[2]
            if account == 1:
                account = "Banco"
            elif account == 2:
                account = "Paypal"
            elif account == 3:
                account = "Skrill"
            bookie = bd.getValue(i[3], "bookie")
            money = i[4]
            if money < 0:
                type = _("Withdrawal to the bank.")
            else:
                type = _("Deposit at bookie")

            item = QTreeWidgetItem([str(sDate), str(id), bookie, type, str(account), str(money) + self.coin])

            items.append(item)

        self.treeMovement.addTopLevelItems(items)

        bd.close()

    def changeItem(self):
        self.itemSelected = self.treeMovement.currentItem().text(1)
        self.mainWindows.enableActions(False)

    def deleteItem(self):
        msg = QMessageBox(self)
        msg.setWindowTitle(_("Remove"))
        msg.setText(_("Are you sure you want to eliminate it?"))
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        msg.setButtonText(QMessageBox.Yes, _("Yes"))
        msg.setButtonText(QMessageBox.No, _("No"))
        resultado = msg.exec()
        if resultado == QMessageBox.Yes:
            bd = Bbdd()
            bd.delete("movement", self.itemSelected)
            data = ["'+bank+'" + self.treeMovement.currentItem().text(5)]
            columns = ["bank"]
            bank_name = self.treeMovement.currentItem().text(4)
            bd.update(columns, data, "bank", "name=?", (bank_name,))
            bd.close()
            self.mainWindows.setCentralWidget(Banks(self.mainWindows))
            self.mainWindows.enableTools("bank")


