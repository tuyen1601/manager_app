from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication, QHeaderView, QTableWidgetItem
from PyQt5 import uic

from datetime import datetime

from pymongo import MongoClient
cluster = "mongodb://10.37.239.135:27017"
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

    def revenue(self):
        self.display()

        timeStart = datetime.strptime(self.dateStart.text(), "%d/%m/%Y %H:%M")
        timeEnd = datetime.strptime(self.dateEnd.text(), "%d/%m/%Y %H:%M")
        card = self.cbbCard.currentText()
        vehicle = self.cbbVehicle.currentText()

        # couting 
        if card == "Tất cả loại vé" and vehicle == "Tất cả loại xe":
            # 1
            documents = in_collection.find({"Loại xe": "Xe máy", "Loại vé": "Vé lượt"})
            for doc in documents:
                if timeStart > timeEnd:
                    self.display()
                else:
                    if timeStart > doc["Thời gian vào"]:
                        self.count1 += 1
                    if timeStart < doc["Thời gian vào"] < timeEnd:
                        self.count2 += 1
                    if timeEnd < doc["Thời gian vào"]:
                        self.count4 +=1
                    if doc["Status"] == "Out":
                        self.count3 += 1
            self.table.setItem(0, 2, QTableWidgetItem(str(self.count1)))
            self.table.setItem(0, 3, QTableWidgetItem(str(self.count2)))
            self.table.setItem(0, 4, QTableWidgetItem(str(self.count3)))
            self.table.setItem(0, 5, QTableWidgetItem(str(self.count4)))

            self.resetCount()

            #2
            documents = in_collection.find({"Loại xe": "Ô tô", "Loại vé": "Vé lượt"})
            for doc in documents:
                if timeStart > timeEnd:
                    self.display()
                else:
                    if timeStart > doc["Thời gian vào"]:
                        self.count1 += 1
                    if timeStart < doc["Thời gian vào"] < timeEnd:
                        self.count2 += 1
                    if timeEnd < doc["Thời gian vào"]:
                        self.count4 +=1
                    if doc["Status"] == "Out":
                        self.count3 += 1
            self.table.setItem(1, 2, QTableWidgetItem(str(self.count1)))
            self.table.setItem(1, 3, QTableWidgetItem(str(self.count2)))
            self.table.setItem(1, 4, QTableWidgetItem(str(self.count3)))
            self.table.setItem(1, 5, QTableWidgetItem(str(self.count4)))

            self.resetCount()

            #3
            documents = in_collection.find({"Loại xe": "Xe máy", "Loại vé": "Vé tháng"})
            for doc in documents:
                if timeStart > timeEnd:
                    self.display()
                else:
                    if timeStart > doc["Thời gian vào"]:
                        self.count1 += 1
                    if timeStart < doc["Thời gian vào"] < timeEnd:
                        self.count2 += 1
                    if timeEnd < doc["Thời gian vào"]:
                        self.count4 +=1
                    if doc["Status"] == "Out":
                        self.count3 += 1
            self.table.setItem(2, 2, QTableWidgetItem(str(self.count1)))
            self.table.setItem(2, 3, QTableWidgetItem(str(self.count2)))
            self.table.setItem(2, 4, QTableWidgetItem(str(self.count3)))
            self.table.setItem(2, 5, QTableWidgetItem(str(self.count4)))

            self.resetCount()

            #4
            documents = in_collection.find({"Loại xe": "Ô tô", "Loại vé": "Vé tháng"})
            for doc in documents:
                if timeStart > timeEnd:
                    self.display()
                else:
                    if timeStart > doc["Thời gian vào"]:
                        self.count1 += 1
                    if timeStart < doc["Thời gian vào"] < timeEnd:
                        self.count2 += 1
                    if timeEnd < doc["Thời gian vào"]:
                        self.count4 +=1
                    if doc["Status"] == "Out":
                        self.count3 += 1
            self.table.setItem(3, 2, QTableWidgetItem(str(self.count1)))
            self.table.setItem(3, 3, QTableWidgetItem(str(self.count2)))
            self.table.setItem(3, 4, QTableWidgetItem(str(self.count3)))
            self.table.setItem(3, 5, QTableWidgetItem(str(self.count4)))

            self.resetCount()

        elif card != "Tất cả loại vé" and vehicle == "Tất cả loại xe":
            if card == "Vé lượt":
                i = 0
                j = 1
            else: 
                i = 2
                j = 3
            #1
            documents = in_collection.find({"Loại vé": card, "Loại xe": "Xe máy"})
            for doc in documents:
                if timeStart > timeEnd:
                    self.display()
                else:
                    if timeStart > doc["Thời gian vào"]:
                        self.count1 += 1
                    if timeStart < doc["Thời gian vào"] < timeEnd:
                        self.count2 += 1
                    if timeEnd < doc["Thời gian vào"]:
                        self.count4 +=1
                    if doc["Status"] == "Out":
                        self.count3 += 1
            self.table.setItem(i, 2, QTableWidgetItem(str(self.count1)))
            self.table.setItem(i, 3, QTableWidgetItem(str(self.count2)))
            self.table.setItem(i, 4, QTableWidgetItem(str(self.count3)))
            self.table.setItem(i, 5, QTableWidgetItem(str(self.count4)))

            self.resetCount()

            #2
            documents = in_collection.find({"Loại vé": card, "Loại xe": "Ô tô"})
            for doc in documents:
                if timeStart > timeEnd:
                    self.display()
                else:
                    if timeStart > doc["Thời gian vào"]:
                        self.count1 += 1
                    if timeStart < doc["Thời gian vào"] < timeEnd:
                        self.count2 += 1
                    if timeEnd < doc["Thời gian vào"]:
                        self.count4 +=1
                    if doc["Status"] == "Out":
                        self.count3 += 1
            self.table.setItem(j, 2, QTableWidgetItem(str(self.count1)))
            self.table.setItem(j, 3, QTableWidgetItem(str(self.count2)))
            self.table.setItem(j, 4, QTableWidgetItem(str(self.count3)))
            self.table.setItem(j, 5, QTableWidgetItem(str(self.count4)))

            self.resetCount()

        elif card == "Tất cả loại vé" and vehicle != "Tất cả loại xe":
            if vehicle == "Xe máy":
                i = 0
                j = 2
            else: 
                i = 1
                j = 3
            #1
            documents = in_collection.find({"Loại vé": "Vé lượt", "Loại xe": vehicle})
            for doc in documents:
                if timeStart > timeEnd:
                    self.display()
                else:
                    if timeStart > doc["Thời gian vào"]:
                        self.count1 += 1
                    if timeStart < doc["Thời gian vào"] < timeEnd:
                        self.count2 += 1
                    if timeEnd < doc["Thời gian vào"]:
                        self.count4 +=1
                    if doc["Status"] == "Out":
                        self.count3 += 1
            self.table.setItem(i, 2, QTableWidgetItem(str(self.count1)))
            self.table.setItem(i, 3, QTableWidgetItem(str(self.count2)))
            self.table.setItem(i, 4, QTableWidgetItem(str(self.count3)))
            self.table.setItem(i, 5, QTableWidgetItem(str(self.count4)))

            self.resetCount()

            #2
            documents = in_collection.find({"Loại vé": "Vé tháng", "Loại xe": vehicle})
            for doc in documents:
                if timeStart > timeEnd:
                    self.display()
                else:
                    if timeStart > doc["Thời gian vào"]:
                        self.count1 += 1
                    if timeStart < doc["Thời gian vào"] < timeEnd:
                        self.count2 += 1
                    if timeEnd < doc["Thời gian vào"]:
                        self.count4 +=1
                    if doc["Status"] == "Out":
                        self.count3 += 1
            self.table.setItem(j, 2, QTableWidgetItem(str(self.count1)))
            self.table.setItem(j, 3, QTableWidgetItem(str(self.count2)))
            self.table.setItem(j, 4, QTableWidgetItem(str(self.count3)))
            self.table.setItem(j, 5, QTableWidgetItem(str(self.count4)))

            self.resetCount()

        else:
            if card == "Vé lượt" and vehicle == "Xe máy":
                i = 0
            elif card == "Vé lượt" and vehicle == "Ô tô":
                i = 1
            elif card == "Vé tháng" and vehicle == "Xe máy":
                i = 2
            else:
                i = 3

            documents = in_collection.find({"Loại vé": card, "Loại xe": vehicle})
            for doc in documents:
                if timeStart > timeEnd:
                    self.display()
                else:
                    if timeStart > doc["Thời gian vào"]:
                        self.count1 += 1
                    if timeStart < doc["Thời gian vào"] < timeEnd:
                        self.count2 += 1
                    if timeEnd < doc["Thời gian vào"]:
                        self.count4 +=1
                    if doc["Status"] == "Out":
                        self.count3 += 1
            self.table.setItem(i, 2, QTableWidgetItem(str(self.count1)))
            self.table.setItem(i, 3, QTableWidgetItem(str(self.count2)))
            self.table.setItem(i, 4, QTableWidgetItem(str(self.count3)))
            self.table.setItem(i, 5, QTableWidgetItem(str(self.count4)))

            self.resetCount()

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


if __name__ == "__main__":
    app = QApplication([])
    revenue = REVENUE()
    revenue.show()
    app.exec_()