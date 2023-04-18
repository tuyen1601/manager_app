from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QPixmap
from PyQt5 import uic

from datetime import datetime

from pymongo import MongoClient
cluster = "mongodb://10.37.239.135:27017"
client = MongoClient(cluster)
db = client.lpr
in_collection = db.in_collection
manager_collection = db.manager_collection


class LOOKUP(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("vehicleLookup.ui", self)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.dateStart.setDate(datetime.now())
        self.dateEnd.setDate(datetime.now())

        self.strCard = "Tất cả loại vé"
        self.strVehicle = "Tất cả loại xe"
        self.strID = ""
        self.strPlate = ""

        #search Card type
        self.cbbCard.activated.connect(self.searchCardType)

        #search Vehicle
        self.cbbVehicle.activated.connect(self.searchVehicle)

        #search Time
        self.dateStart.dateTimeChanged.connect(self.searchTime)
        self.dateEnd.dateTimeChanged.connect(self.searchTime)

        #search Card
        self.lnCard.textChanged.connect(self.searchCard)

        #search Plate
        self.lnPlate.textChanged.connect(self.searchPlate)

        #display Image
        self.table.itemClicked.connect(self.displayImage)

        self.displayTable()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def display(self, data):
        self.table.insertRow(0)
        self.table.setItem(0, 0, QTableWidgetItem(data["Mã thẻ"]))
        self.table.setItem(0, 1, QTableWidgetItem(data["Biển số"]))
        self.table.setItem(0, 2, QTableWidgetItem(data["Loại vé"]))
        self.table.setItem(0, 3, QTableWidgetItem(data["Loại xe"]))
        doc = manager_collection.find_one({"Mã thẻ": data["Mã thẻ"]}) 
        if doc:
            self.table.setItem(0, 4, QTableWidgetItem(doc["Chủ xe"]))

    def displayTable(self):
        self.table.setRowCount(0)
        for data in in_collection.find({}):
            self.display(data)
        self.countVehicle()

    def searchCardType(self):
        self.strCard = self.cbbCard.currentText()
        if self.strVehicle != "Tất cả loại xe":
            if self.strCard != "Tất cả loại vé":
                self.table.setRowCount(0)
                for data in in_collection.find({}):
                    if data["Loại vé"] == self.strCard and data["Loại xe"] == self.strVehicle:
                        self.display(data)
            else:
                self.table.setRowCount(0)
                for data in in_collection.find({}):
                    if data["Loại xe"] == self.strVehicle:
                        self.display(data)
        else:
            if self.strCard != "Tất cả loại vé":
                self.table.setRowCount(0)
                for data in in_collection.find({}):
                    if data["Loại vé"] == self.strCard:
                        self.display(data)
            else:
                self.displayTable()

    def searchVehicle(self):
        self.strVehicle = self.cbbVehicle.currentText()
        if self.strCard != "Tất cả loại vé":
            if self.strVehicle != "Tất cả loại xe":
                self.table.setRowCount(0)
                for data in in_collection.find({}):
                    if data["Loại vé"] == self.strCard and data["Loại xe"] == self.strVehicle:
                        self.display(data)
            else:
                self.table.setRowCount(0)
                for data in in_collection.find({}):
                    if data["Loại vé"] == self.strCard:
                        self.display(data)
        else: 
            if self.strVehicle != "Tất cả loại xe":
                self.table.setRowCount(0)
                for data in in_collection.find({}):
                    if data["Loại xe"] == self.strVehicle:
                        self.display(data)
            else:
                self.displayTable()

    def searchTime(self):
        timeStart = datetime.strptime(self.dateStart.text(), "%d/%m/%Y %H:%M")
        timeEnd = datetime.strptime(self.dateEnd.text(), "%d/%m/%Y %H:%M")

        for row, data in zip(range(self.table.rowCount()), in_collection.find({})):
            timeIN = data["Thời gian vào"]
            if timeIN >= timeStart and timeIN <= timeEnd:
                self.table.setRowHidden(row, False)
            else:
                self.table.setRowHidden(row, True)

    def searchCard(self):
        self.strID = self.lnCard.text().lower()
        self.strPlate = self.lnPlate.text().lower()
        if self.strPlate != "":
            if self.strID != "":
                self.table.setRowCount(0)
                for data in in_collection.find({}):
                    if not str(data["Mã thẻ"]).find(self.strID) and not str(data["Biển số"]).find(self.strPlate):
                        self.display(data)
            else:
                self.table.setRowCount(0)
                for data in in_collection.find({}):
                    if not str(data["Biển số"]).find(self.strPlate):
                        self.display(data)
        else: 
            if self.strID != "":
                self.table.setRowCount(0)
                for data in in_collection.find({}):
                    if not str(data["Mã thẻ"]).find(self.strID):
                        self.display(data)
            else:
                self.displayTable()

    def searchPlate(self):
        self.strPlate = self.lnPlate.text().lower()
        self.strID = self.lnCard.text().lower()
        if self.strID != "":
            if self.strPlate != "":
                self.table.setRowCount(0)
                for data in in_collection.find({}):
                    if not str(data["Mã thẻ"]).find(self.strID) and not str(data["Biển số"]).find(self.strPlate):
                        self.display(data)
            else:
                self.table.setRowCount(0)
                for data in in_collection.find({}):
                    if not str(data["Mã thẻ"]).find(self.strID):
                        self.display(data)
        else: 
            if self.strPlate != "":
                self.table.setRowCount(0)
                for data in in_collection.find({}):
                    if not str(data["Biển số"]).find(self.strPlate):
                        self.display(data)
            else:
                self.displayTable()

    def displayImage(self):
        row = self.table.currentRow()
        ID = self.table.item(row, 0).text()
        data = in_collection.find_one({"Mã thẻ": ID})
        self.lblImg.setScaledContents(True)
        self.lblImg.setPixmap(QPixmap(data["Image Path"]))

    def countVehicle(self):
        countMotobike = 0
        countCar = 0
        for data in in_collection.find({}):
            if data["Loại xe"] == "Xe máy":
                countMotobike += 1
            if data["Loại xe"] == "Ô tô":
                countCar += 1
        
        self.lblCar.setText(str(countCar))
        self.lblMtb.setText(str(countMotobike))
        

if __name__ == "__main__":
    app = QApplication([])
    lookup = LOOKUP()
    lookup.show()
    app.exec_()