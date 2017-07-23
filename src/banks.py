import sys
from PyQt5.QtWidgets import QMessageBox, QWidget, QTreeWidgetItem
from PyQt5 import uic
sys.path.append("./lib")
from bbdd import Bbdd
from bookie import Bookie



class Banks(QWidget):
    def __init__(self, mainWindows):
        QWidget.__init__(self)
        uic.loadUi("../ui/banks.ui", self)
        self.mainWindows = mainWindows
        mainWindows.aNew.triggered.connect(mainWindows.newBank)
        self.mainWindows.setWindowTitle("Bank | Betcon")
        self.initData()
        self.initTree()

    def initData(self):
        bd = Bbdd()

        # CC
        cc = bd.select("bank", None, "id=1", "bank")
        cc = cc[0][0]
        self.txtCc.setText(str(cc))

        # Paypal
        paypal = bd.select("bank", None, "id=2", "bank")
        paypal = paypal[0][0]
        self.txtPaypal.setText(str(paypal))

        # CC
        skrill = bd.select("bank", None, "id=3", "bank")
        skrill = skrill[0][0]
        self.txtSkrill.setText(str(skrill))

        self.txtTotal.setText(str(cc+paypal+skrill))

    def initTree(self):
        self.treeBookie.clear()
        data = Bookie.selectAll()

        items = []
        for i in data:
            item = QTreeWidgetItem([i.name])
            items.append(item)

        self.treeBookie.addTopLevelItems(items)


