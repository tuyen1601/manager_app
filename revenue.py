from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication, QHeaderView, QTableWidgetItem
from PyQt5 import uic

from datetime import datetime

from pymongo import MongoClient
cluster = "mongodb+srv://tuyennt:0711@lpr.3u3tc8j.mongodb.net/test"
client = MongoClient(cluster)
db = client.lpr
in_collection = db.in_collection
out_collection = db.out_collection


class REVENUE(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("revenue.ui", self)

        self.dateStart.setDate(datetime.now())
        self.dateEnd.setDate(datetime.now())

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.count1 = 0
        self.count2 = 0
        self.count3 = 0
        self.count4 = 0

        self.display()

        self.btn.clicked.connect(self.revenue)
        self.btn.clicked.connect(self.sumCard)
        self.btn.clicked.connect(self.calculateRevenue)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def display(self):
        self.table.setRowCount(7)
        self.table.setItem(0, 0, QTableWidgetItem("Xe máy"))
        self.table.setItem(1, 0, QTableWidgetItem("Ô tô"))
        self.table.setItem(2, 0, QTableWidgetItem("Xe máy"))
        self.table.setItem(3, 0, QTableWidgetItem("Ô tô"))
        self.table.setItem(4, 0, QTableWidgetItem("Tổng vé lượt"))
        self.table.setItem(5, 0, QTableWidgetItem("Tổng vé tháng"))
        self.table.setItem(6, 0, QTableWidgetItem("Tổng cộng"))

        self.table.setItem(0, 1, QTableWidgetItem("Vé lượt"))
        self.table.setItem(1, 1, QTableWidgetItem("Vé lượt"))
        self.table.setItem(2, 1, QTableWidgetItem("Vé tháng"))
        self.table.setItem(3, 1, QTableWidgetItem("Vé tháng"))

        for i in range(self.table.rowCount()):
            self.table.setItem(i, 2, QTableWidgetItem("0"))
            self.table.setItem(i, 3, QTableWidgetItem("0"))
            self.table.setItem(i, 4, QTableWidgetItem("0"))
            self.table.setItem(i, 5, QTableWidgetItem("0"))
            self.table.setItem(i, 6, QTableWidgetItem("0"))

    def resetCount(self):
        self.count1 = 0
        self.count2 = 0
        self.count3 = 0
        self.count4 = 0

    def revenueEachRow(self, i, timeStart, timeEnd, vehicle, card):
        documents = out_collection.find({"Loại xe": vehicle, "Loại vé": card})
        for doc in documents:
            if timeStart > timeEnd:
                self.display()
            else:
                if timeStart > doc["Thời gian vào"]:
                    self.count1 += 1
                if timeStart < doc["Thời gian vào"] < timeEnd:
                    self.count2 += 1
                if timeEnd > doc["Thời gian ra"]:
                    self.count3 += 1
                if timeEnd < doc["Thời gian vào"]:
                    self.count4 +=1
        self.table.setItem(i, 2, QTableWidgetItem(str(self.count1)))
        self.table.setItem(i, 3, QTableWidgetItem(str(self.count2)))
        self.table.setItem(i, 4, QTableWidgetItem(str(self.count3)))
        self.table.setItem(i, 5, QTableWidgetItem(str(self.count4)))

        self.resetCount()

    def revenue(self):
        self.display()

        timeStart = datetime.strptime(self.dateStart.text(), "%d/%m/%Y %H:%M")
        timeEnd = datetime.strptime(self.dateEnd.text(), "%d/%m/%Y %H:%M")
        cardSelected = self.cbbCard.currentText()
        vehicleSelected = self.cbbVehicle.currentText()

        if cardSelected == "Tất cả loại vé" and vehicleSelected == "Tất cả loại xe":
            for i in range(4):
                vehicle = self.table.item(i, 0).text()
                card = self.table.item(i, 1).text()
                self.revenueEachRow(i, timeStart, timeEnd, vehicle, card)
        elif cardSelected == "Tất cả loại vé":
            if vehicleSelected == "Xe máy":
                for i in [0, 2]:
                    card = self.table.item(i, 1).text()
                    self.revenueEachRow(i, timeStart, timeEnd, vehicleSelected, card)
            else:
                for i in [1, 3]:
                    card = self.table.item(i, 1).text()
                    self.revenueEachRow(i, timeStart, timeEnd, vehicleSelected, card)
        elif vehicleSelected == "Tất cả loại xe":
            if cardSelected == "Vé lượt":
                for i in [0, 1]:
                    vehicle = self.table.item(i, 0).text()
                    self.revenueEachRow(i, timeStart, timeEnd, vehicle, cardSelected)
            else:
                for i in [2, 3]:
                    vehicle = self.table.item(i, 0).text()
                    self.revenueEachRow(i, timeStart, timeEnd, vehicle, cardSelected)
        else:
            for i in range(4):
                vehicle = self.table.item(i, 0).text()
                card = self.table.item(i, 1).text()

                if vehicle == vehicleSelected and card == cardSelected:
                    self.revenueEachRow(i, timeStart, timeEnd, vehicleSelected, cardSelected)
                    
        # canculate sum card
        sumDay = 0
        sumMonth = 0
        for i in range(2, 6):
            for j in range(0, 2):
                sumDay += int(self.table.item(j, i).text())
            self.table.setItem(4, i, QTableWidgetItem(str(sumDay)))
            sumDay = 0
            for k in range(2, 4):
                sumMonth += int(self.table.item(k, i).text())
            self.table.setItem(5, i, QTableWidgetItem(str(sumMonth)))
            sumMonth = 0

    def sumCard(self):
        sumCard = 0
        for i in range(2, 6):
            for j in range(4, 6):
                sumCard += int(self.table.item(j, i).text())
            self.table.setItem(6, i, QTableWidgetItem(str(sumCard)))
            sumCard = 0

    def calculateCar(self, timeStart, timeEnd):
        documentCar = out_collection.find({"Loại xe": "Ô tô", "Loại vé": "Vé lượt"})
        sumCar = 0
        for doc in documentCar:
            if timeStart <= doc["Thời gian vào"] and timeEnd >= doc["Thời gian ra"]:
                sumCar += doc["Giá vé"]

        return sumCar 

    def calculateMotobike(self, timeStart, timeEnd):
        documentMotobike = out_collection.find({"Loại xe": "Xe máy", "Loại vé": "Vé lượt"})
        sumMotobike = 0
        for doc in documentMotobike:
            if timeStart <= doc["Thời gian vào"] and timeEnd >= doc["Thời gian ra"]:
                sumMotobike += doc["Giá vé"]

        return sumMotobike

    def calculateRevenue(self):
        timeStart = datetime.strptime(self.dateStart.text(), "%d/%m/%Y %H:%M")
        timeEnd = datetime.strptime(self.dateEnd.text(), "%d/%m/%Y %H:%M")
        card = self.cbbCard.currentText()
        vehicle = self.cbbVehicle.currentText()

        sumCar = self.calculateCar(timeStart, timeEnd)
        sumMotobike = self.calculateMotobike(timeStart, timeEnd)

        if card != "Vé tháng" and vehicle == "Tất cả loại xe":
            self.table.setItem(1, 6, QTableWidgetItem(str(sumCar)))
            self.table.setItem(0, 6, QTableWidgetItem(str(sumMotobike)))

            self.table.setItem(4, 6, QTableWidgetItem(str(sumMotobike + sumCar)))
            self.table.setItem(6, 6, QTableWidgetItem(str(sumMotobike + sumCar)))
        elif card != "Vé tháng" and vehicle == "Xe máy":
            self.table.setItem(0, 6, QTableWidgetItem(str(sumMotobike)))

            self.table.setItem(4, 6, QTableWidgetItem(str(sumMotobike)))
            self.table.setItem(6, 6, QTableWidgetItem(str(sumMotobike)))
        elif card != "Vé tháng" and vehicle == "Ô tô":
            self.table.setItem(0, 6, QTableWidgetItem(str(sumCar)))

            self.table.setItem(4, 6, QTableWidgetItem(str(sumCar)))
            self.table.setItem(6, 6, QTableWidgetItem(str(sumCar)))


if __name__ == "__main__":
    app = QApplication([])
    revenue = REVENUE()
    revenue.show()
    app.exec_()