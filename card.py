from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication, QHeaderView, QTableWidgetItem, QFileDialog, QMessageBox
from PyQt5 import uic
import re
import pandas as pd

from addCard import ADDCARD

from pymongo import MongoClient

cluster = "mongodb://10.37.239.135:27017"
client = MongoClient(cluster)
db = client.lpr
card = db.card # type(card) == <class 'pymongo.collection.Collection'>
manager_collection = db.manager_collection

def add2Card(id, typeCard):
    db = {"Mã thẻ": id, "Trạng thái": "Chưa sử dụng", "Biển số": "", "Loại thẻ": typeCard}
    card.insert_one(db)

def checkID(id):
    return card.find_one({"Mã thẻ": id})

class CARD(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("card.ui", self)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.addCard = ADDCARD()

        # 1a. Display
        self.displayTable()

        # 1b. Add new card
        self.btnAdd.clicked.connect(self.displayAddNew)
        self.addCard.btnOK.clicked.connect(self.addNew)

        # 1c. Import file
        self.btnImport.clicked.connect(self.showSelectedOpenFile)
        
        # 1d. Delete card
        self.btnDelete.clicked.connect(self.deleteCard)

        # 1e. Filter the cards
        self.lnCard.textChanged.connect(self.filterByID)
        self.lnPlate.textChanged.connect(self.filterByPlate)
        self.cbbStatus.activated.connect(self.filterByStatus)

        self.regex_id = re.compile('', re.IGNORECASE)
        self.regex_textLP = re.compile('', re.IGNORECASE)
        self.regex_status = re.compile('', re.IGNORECASE)   

    # Align
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 1a. DisplayList
    def display(self, data, table): # type(find_result) == <class 'pymongo.cursor.Cursor'>
        table.insertRow(0)
        table.setItem(0, 0, QTableWidgetItem(data["Mã thẻ"]))
        table.setItem(0, 1, QTableWidgetItem(data["Trạng thái"]))
        table.setItem(0, 2, QTableWidgetItem(data["Biển số"]))

    def displayTable(self): # type(find_result) == <class 'pymongo.cursor.Cursor'>
        self.table.setRowCount(0)
        self.table2.setRowCount(0)
        for data in card.find({}):
            if data["Loại thẻ"] == "Thẻ tháng":
                self.display(data, self.table)
            else:
                self.display(data, self.table2)

    def displayFilter(self, find_filter):
        self.table.setRowCount(0)
        self.table2.setRowCount(0)
        for data in find_filter:
            if data["Loại thẻ"] == "Thẻ tháng":
                self.display(data, self.table)
            else:
                self.display(data, self.table2)


    # 1b. Add single new
    def displayAddNew(self):
        self.addCard.btnOK.setEnabled(True)

        self.addCard.lnCard.clear()
        self.addCard.lblMessage.setText("")

        self.addCard.lnCard.setEnabled(True)

        self.addCard.show()

    def addNew(self):
        id = self.addCard.lnCard.text().upper()
        self.addCard.lblMessage.setText("")
        if id == "":
            self.addCard.lblMessage.setText("Vui lòng nhập mã thẻ")
            self.addCard.lblMessage.setStyleSheet("color: red")
        else:
            check = checkID(id)
            if check is None:
                self.addCard.lblMessage.setText("Đăng ký thành công")
                self.addCard.lblMessage.setStyleSheet("color: green")
                typeCard_addNew = self.addCard.cbbType.currentText()
                add2Card(id, typeCard_addNew)
                self.addCard.lnCard.clear()
            else:
                self.addCard.lblMessage.setText("Thẻ đã tồn tại")
                self.addCard.lblMessage.setStyleSheet("color: red")
        
        self.resetFilter()
        self.displayTable()

    # 1c. Import file
    def showSelectedOpenFile(self):
        fname = QFileDialog.getOpenFileName(self, "Open File", "", "Excel Files (*xlsx)")

        if fname[0]:
            success_count = 0
            sum_count = 0

            df = pd.read_excel(fname[0], sheet_name='Sheet1')
            sum_count = df.shape[0]
            for _, row in df.iterrows():
                excel_id = str(row[0])
                excel_type = str(row[1])

                if checkID(excel_id) == None:
                    success_count += 1
                    add2Card(excel_id, excel_type)
            
            self.resetFilter()
            self.displayTable()
            self.messageCheckRegis(success_count, sum_count)
    
    def messageCheckRegis(self, success_count, sum_count):
        message = QMessageBox()
        message.setWindowTitle("Message")
        message.setText("Đã thêm thành công {}/{} thẻ".format(success_count, sum_count))
        message.setIcon(QMessageBox.Information)
        message.exec_()
    
    # 1d. Delete single card
    def deleteCard(self):
        selected = self.table.selectionModel().selectedRows()
        selected2 = self.table2.selectionModel().selectedRows()
        if selected:
            for i in range(len(selected)):
                row = selected[0].row()
                id = self.table.item(row, 0).text()
                card.delete_one({"Mã thẻ": id})
                manager_collection.delete_one({"Mã thẻ": id})
                self.table.removeRow(row)
                i += 1
            self.resetFilter()
        if selected2:
            for i in range(len(selected2)):
                row = selected2[0].row()
                id = self.table2.item(row, 0).text()
                card.delete_one({"Mã thẻ": id})
                manager_collection.delete_one({"Mã thẻ": id})
                self.table2.removeRow(row)
                i += 1
            self.resetFilter()
        # self.displayTable()

    # 1e. Filter
    def filterByID(self):
        id = self.lnCard.text()
        self.regex_id = re.compile(f'.*{id}.*', re.IGNORECASE)
        self.displayFilter(card.find({"Mã thẻ": self.regex_id, "Biển số": self.regex_textLP, "Trạng thái": self.regex_status}))

    def filterByPlate(self):
        textLP = self.lnPlate.text()
        self.regex_textLP = re.compile(f'.*{textLP}.*', re.IGNORECASE)
        self.displayFilter(card.find({"Mã thẻ": self.regex_id, "Biển số": self.regex_textLP, "Trạng thái": self.regex_status}))

    def filterByStatus(self):
        self.regex_status = self.cbbStatus.currentText()
        if self.regex_status == "Tất cả":
            self.regex_status = re.compile('', re.IGNORECASE)
            self.displayFilter(card.find({"Mã thẻ": self.regex_id, "Biển số": self.regex_textLP, "Trạng thái": self.regex_status}))
        else:
            self.displayFilter(card.find({"Mã thẻ": self.regex_id, "Biển số": self.regex_textLP, "Trạng thái": self.regex_status}))

    def resetFilter(self):
        self.lnCard.setText("")
        self.lnPlate.setText("")
        self.cbbStatus.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication([])
    b = CARD()
    b.show()
    app.exec_()