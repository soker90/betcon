import sys
import os
import inspect
from PySide6.QtWidgets import QMessageBox, QWidget, QAbstractItemView
from uiloader import loadUi
from table_model import BetconTableModel, make_item, paint_row_items
directory = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
sys.path.append(directory + "/lib")

from bbdd import Bbdd
from gettext import gettext as _
import gettext
from libyaml import LibYaml


class Tipsters(QWidget):
    def __init__(self, mainWindows):
        QWidget.__init__(self)
        loadUi(directory + "/../ui/tipsters.ui", self)
        gettext.textdomain("betcon")
        gettext.bindtextdomain("betcon", "../lang/mo" + mainWindows.lang)
        gettext.bindtextdomain("betcon", "/usr/share/locale" + mainWindows.lang)
        self.mainWindows = mainWindows
        mainWindows.diconnectActions()
        mainWindows.aNew.triggered.connect(mainWindows.newTipster)
        self.mainWindows.setWindowTitle(_("Tipsters") + " | Betcon v" + mainWindows.version)
        self.model = BetconTableModel()
        self.treeMain.setModel(self.model)
        self.treeMain.setColumnHidden(1, True)
        self.treeMain.setAlternatingRowColors(True)
        self.treeMain.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.treeMain.horizontalHeader().setStretchLastSection(True)
        self.treeMain.verticalHeader().setVisible(False)
        self.treeMain.setSortingEnabled(True)

        self.coin = LibYaml().interface["coin"]

        self.translate()
        self.initTree()

        self.treeMain.selectionModel().selectionChanged.connect(self.changeItem)
        self.mainWindows.aEdit.triggered.connect(self.editItem)
        self.mainWindows.aRemove.triggered.connect(self.deleteItem)
        self.itemSelected = -1

    def translate(self):
        header = [_("Name"), "index", _("Cost"), _("Profit of the bets"), _("Balance")]

        self.model.setHorizontalHeaderLabels(header)

    def initTree(self):
        bd = Bbdd()
        money = {}

        data = bd.select("conjunta")

        for i in data:
            data2 = bd.select("conjunta_tipster", None, "conjunta=" + str(i[0]))
            if len(data2) > 1:
                money_tipster = i[4]/len(data2)
                for j in data2:
                    try:
                        money[j[1]] += money_tipster
                    except KeyError:
                        money[j[1]] = money_tipster

        data = bd.select("tipster", "name")

        for i in data:
            id = i[0]
            name = i[1]
            cost = bd.sum("tipster_month", "money", "tipster=" + str(id))
            if id in money.keys():
                cost += money[id]

            profit = bd.sum("bet", "profit", "tipster=" + str(id))
            balance = profit - cost

            if cost == 0:
                cost = "--" + self.coin
            else:
                cost = "{0:.2f}".format(cost) + self.coin
            profit = "{0:.2f}".format(profit) + self.coin
            balance = "{0:.2f}".format(balance) + self.coin
            row = [make_item(name), make_item(str(id)), make_item(cost), make_item(profit), make_item(balance)]
            paint_row_items(row, float(bd.sum("bet", "profit", "tipster=" + str(id))), 1)
            self.model.appendRow(row)

        bd.close()

    def changeItem(self):
        indexes = self.treeMain.selectionModel().selectedRows()
        if not indexes:
            return
        self.itemSelected = self.model.get_id(indexes[0].row())
        self.mainWindows.enableActions()

    def editItem(self):
        self.mainWindows.editTipster(self.itemSelected)

    def deleteItem(self):
        resultado = QMessageBox.question(self, _("Remove"),
                                         _("Are you sure you want to eliminate this tipster and all associated bets?"),
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if resultado == QMessageBox.Yes:
            bd = Bbdd()
            bd.delete("tipster", self.itemSelected)
            bd.deleteWhere("bet", "tipster=" + str(self.itemSelected))
            self.mainWindows.setCentralWidget(Tipsters(self.mainWindows))
            self.mainWindows.enableTools()

