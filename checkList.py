from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QHeaderView, QTableWidgetItem
from PyQt5 import uic

from pymongo import MongoClient
cluster = "mongodb://10.37.239.135:27017"
client = MongoClient(cluster)
db = client.lpr
manager_collection = db.manager_collection


class CHECKLIST(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("checkList.ui", self)

        self.items = 0
        self.tableMonth.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableDay.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tab.currentChanged.connect(self.tabChanged)
        self.tab.setTabText(0, "Vé tháng")
        self.tab.setTabText(1, "Vé ngày")
        self.displayList()
        self.lnSearch.textChanged.connect(self.search)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def tabChanged(self):
        pass

    def displayList(self):
        for data in manager_collection.find({}):
            self.tableMonth.insertRow(self.items)
            self.tableDay.insertRow(self.items)
            if data["Loại vé"] == "Vé tháng":
                self.tableMonth.setItem(self.items, 0, QTableWidgetItem(data["ID"]))
                self.tableMonth.setItem(self.items, 1, QTableWidgetItem(data["Biển số"]))
                self.tableMonth.setItem(self.items, 2, QTableWidgetItem(data["Loại phương tiện"]))
                self.tableMonth.setItem(self.items, 3, QTableWidgetItem(data["Loại vé"]))
                self.tableMonth.setItem(self.items, 4, QTableWidgetItem(data["Ngày đăng ký"]))
                self.tableMonth.setItem(self.items, 5, QTableWidgetItem(data["Ngày hết hạn"]))
            else:
                self.tableDay.setItem(self.items, 0, QTableWidgetItem(data["ID"]))
                self.tableDay.setItem(self.items, 3, QTableWidgetItem(data["Loại vé"]))
            self.items += 1
            
    def search(self):
        strSearch = self.lnSearch.text().lower()
        for row in range(self.tableMonth.rowCount()):
            item = self.tableMonth.item(row, 0)
            if item is not None:
                self.tableMonth.setRowHidden(row, strSearch not in item.text().lower())
            else:
                self.tableMonth.setRowHidden(row, True)
