import sys, os, inspect
from PyQt5.QtWidgets import QMessageBox, QWidget, QTreeWidgetItem
from PyQt5 import uic
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")
from bbdd import Bbdd
from bookie import Bookie
from datetime import datetime, date



class Banks(QWidget):
    def __init__(self, mainWindows):
        QWidget.__init__(self)
        uic.loadUi(directory + "/../ui/banks.ui", self)
        self.mainWindows = mainWindows
        mainWindows.diconnectActions()
        mainWindows.aNew.triggered.connect(mainWindows.newBank)
        self.mainWindows.setWindowTitle("Bank | Betcon v" + mainWindows.version)
        self.treeMovement.itemSelectionChanged.connect(self.changeItem)
        self.initData()
        self.initTree()
        self.treeMovement.header().hideSection(1)
        self.mainWindows.aRemove.triggered.connect(self.deleteItem)

        self.itemSelected = -1

    def initData(self):
        self.txtDeposit.setText("{0:.2f}".format(Bookie.sumAll("money>0")))
        self.txtTakeOut.setText("{0:.2f}".format(Bookie.sumAll("money<0")))
        bookies = Bookie.sumAll()
        bonus = Bookie.sumBonus()
        self.txtBonus.setText("{0:.2f}".format(bonus))
        self.txtBookie.setText("{0:.2f}".format(bookies + bonus))

        bd = Bbdd()

        tipsters = bd.sum("tipster_month", "money")
        conjuntas = bd.sum("conjunta", "money")
        self.txtTipster.setText(str(tipsters + conjuntas))
        profits = bd.sum("bet", "profit") + bonus
        self.txtProfit.setText("{0:.2f}".format(profits - tipsters - conjuntas))
        bets = bd.sum("bet", "bet")
        try:
            yields = "{0:.2f}%".format((profits/bets)*100)
        except ZeroDivisionError:
            yields = "0.0%"
        self.txtYield.setText(yields)

        # CC
        cc = bd.select("bank", None, "id=1", "bank")
        cc = cc[0][0]
        self.txtCc.setText("{0:.2f}".format(cc))

        # Paypal
        paypal = bd.select("bank", None, "id=2", "bank")
        paypal = paypal[0][0]
        self.txtPaypal.setText("{0:.2f}".format(paypal))

        # SKRILL
        skrill = bd.select("bank", None, "id=3", "bank")
        skrill = skrill[0][0]
        self.txtSkrill.setText("{0:.2f}".format(skrill))

        total = "{0:.2f}".format(cc+paypal+skrill+bonus+bookies)
        self.txtTotal.setText(total)

    def initTree(self):

        self.treeBookie.clear()
        data = Bookie.selectAll()

        items = []
        for i in data:
            bank = Bookie.sumAll("bookie=" + str(i.id))
            bank = 0.0 if bank is None else bank
            bonus = Bookie.sumBonus("bookie=" + str(i.id))
            bonus = 0.0 if bonus is None else bonus
            bank += bonus
            item = QTreeWidgetItem([i.name, "{0:.2f}".format(bank)])
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
            except:
                sDate = datetime.strptime(i[1], "%d/%m/%Y") #Fix for Windows
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
                type = "Retirada en cuenta"
            else:
                type = "Depósito en casa"

            item = QTreeWidgetItem([str(sDate), str(id), bookie, type, str(account), str(money)])

            items.append(item)

        self.treeMovement.addTopLevelItems(items)

        bd.close()

    def changeItem(self):
        self.itemSelected = self.treeMovement.currentItem().text(1)
        self.mainWindows.enableActions(False)

    def deleteItem(self):
        resultado = QMessageBox.question(self, "Eliminar", "¿Estas seguro que desas eliminarlo?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if resultado == QMessageBox.Yes:
            bd = Bbdd()
            bd.delete("movement", self.itemSelected)
            data = ["'+bank+'" + self.treeMovement.currentItem().text(5)]
            columns = ["bank"]
            bd.update(columns, data, "bank", "name='" + self.treeMovement.currentItem().text(4)+"'")
            bd.close()
            self.mainWindows.setCentralWidget(Banks(self.mainWindows))
            self.mainWindows.enableTools("bank")


