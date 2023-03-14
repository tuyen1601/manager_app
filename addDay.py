from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDesktopWidget
from PyQt5 import uic

from pymongo import MongoClient
cluster = "mongodb://10.37.239.135:27017"
client = MongoClient(cluster)
db = client.lpr
manager_collection = db.manager_collection

def message_warning():
    message = QMessageBox()
    message.setWindowTitle("Message")
    message.setText("Error")
    message.setIcon(QMessageBox.Warning)
    message.exec_()

def message_information():
    message = QMessageBox()
    message.setWindowTitle("Message")
    message.setText("OK")
    message.setIcon(QMessageBox.Information)
    message.exec_()

def add2Manager(iD, vehicle):
    db = {"ID": iD, "Vehicle": vehicle, "Loại vé": "Vé ngày"}
    manager_collection.insert_one(db)


class ADDDAY(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("addDay.ui", self)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def addNew(self):
        iD = self.txtID.toPlainText()
        if self.rbCar.isChecked():
            vehicle = self.rbCar.text()
        else:
            vehicle = self.rbMotobike.text()
        if iD == "":
            message_warning()
        elif self.rbCar.isChecked() == False and self.rbMotobike.isChecked() == False:
            message_warning()
        else:
            message_information()
            add2Manager(iD, vehicle)
            self.txtID.clear()
