from datetime import datetime

from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QMessageBox
from PyQt5 import uic

from pymongo import MongoClient
cluster = "mongodb://localhost:27017"
client = MongoClient(cluster)
db = client.lpr
manager_collection = db.manager_collection

def add2Manager(iD, textLP, regisDate, expiredDate):
    db = {"ID": iD, "Licence Plate": textLP, "Registration Date": regisDate, "Expiration Date": expiredDate}
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


class ADD(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("addLP.ui", self)

        self.btnOK.clicked.connect(self.addNew)
        self.dateRegis.setDate(datetime.now().date())
        self.dateExpired.setDate(datetime.now().date())

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def addNew(self):
        textLP = self.txtLP.toPlainText()
        iD = self.txtID.toPlainText()
        regisDate = self.dateRegis.text()
        expiredDate = self.dateExpired.text()
        if textLP == "" or iD == "":
            message_warning()
        else:
            message_information()
            dbManager = add2Manager(iD, textLP, regisDate, expiredDate)
            self.txtLP.clear()
            self.txtID.clear()

