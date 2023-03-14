from datetime import datetime

from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QMessageBox
from PyQt5 import uic

from pymongo import MongoClient
cluster = "mongodb://10.37.239.135:27017"
client = MongoClient(cluster)
db = client.lpr
manager_collection = db.manager_collection

def add2Manager(iD, textLP, Vehicle, regisDate, expiredDate):
    db = {"ID": iD, "Biển số": textLP, "Loại phương tiện": Vehicle, "Loại vé": "Vé tháng", "Ngày đăng ký": regisDate, "Ngày hết hạn": expiredDate}
    manager_collection.insert_one(db)

    return db

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


class ADDMONTH(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("addMonth.ui", self)

        self.dateRegis.setDate(datetime.now().date())
        self.dateExpired.setDate(datetime.now().date())

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def addNew(self):
        textLP = self.txtLP.toPlainText().upper()
        iD = self.txtID.toPlainText()
        regisDate = self.dateRegis.text()
        expiredDate = self.dateExpired.text()
        if self.rbCar.isChecked():
            Vehicle = self.rbCar.text()
        else:
            Vehicle = self.rbMotobike.text()
        if textLP == "" or iD == "":
            message_warning()
        elif self.rbCar.isChecked() == False and self.rbMotobike.isChecked() == False:
            message_warning()
        elif regisDate >= expiredDate:
            message_warning()
        else:
            message_information()
            dbManager = add2Manager(iD, textLP, Vehicle,regisDate, expiredDate)
            self.txtLP.clear()
            self.txtID.clear()

