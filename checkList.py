from datetime import datetime

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

        #display row
        self.displayList()

        #search
        self.lnSearch.textChanged.connect(self.search)

        #delete row
        self.btnDelete.clicked.connect(self.removeRow)

        #update row
        # self.btnUpdate.clicked.connect(self.updateRow)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def displayList(self):
        for data in manager_collection.find({}):
            if data["Loại vé"] == "Vé tháng":
                self.tableMonth.insertRow(self.items)
                self.tableMonth.setItem(self.items, 0, QTableWidgetItem(data["ID"]))
                self.tableMonth.setItem(self.items, 1, QTableWidgetItem(data["Biển số"]))
                self.tableMonth.setItem(self.items, 2, QTableWidgetItem(data["Loại phương tiện"]))
                self.tableMonth.setItem(self.items, 3, QTableWidgetItem(data["Loại vé"]))
                self.tableMonth.setItem(self.items, 4, QTableWidgetItem(data["Ngày đăng ký"]))
                self.tableMonth.setItem(self.items, 5, QTableWidgetItem(data["Ngày hết hạn"]))
                #check time 
                objDateRegis = datetime.strptime(data["Ngày đăng ký"], "%d %m %Y")
                objDateExpired = datetime.strptime(data["Ngày hết hạn"], "%d %m %Y")
                dateNow = datetime.now()
                if dateNow >= objDateRegis and dateNow <= objDateExpired:
                    self.tableMonth.setItem(self.items, 6, QTableWidgetItem("Chưa hết hạn"))
                else:
                    self.tableMonth.setItem(self.items, 6, QTableWidgetItem("Hết hạn"))

                continue

            self.tableDay.insertRow(self.items)
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
        for row in range(self.tableDay.rowCount()):
            item = self.tableDay.item(row, 0)
            if item is not None:
                self.tableDay.setRowHidden(row, strSearch not in item.text().lower())
            else:
                self.tableDay.setRowHidden(row, True)

    def removeRow(self):
        selectedMonth = self.tableMonth.selectionModel().selectedRows()
        selectedDay = self.tableDay.selectionModel().selectedRows()
        if selectedMonth:
            row = selectedMonth[0].row()
            iD = self.tableMonth.item(row, 0).text()
            manager_collection.delete_one({"ID": iD})
            self.tableMonth.removeRow(row)
        if selectedDay:
            row = selectedDay[0].row()
            iD = self.tableDay.item(row, 0).text()
            manager_collection.delete_one({"ID": iD})
            self.tableDay.removeRow(row)

    def updateRow(self):
        pass
