from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QMessageBox
from PyQt5 import uic

from pymongo import MongoClient
cluster = "mongodb://localhost:27017"
client = MongoClient(cluster)
db = client.lpr
manager_collection = db.manager_collection

def send2Manager(iD, textLP, regis_date, expired_date):
    db = {"ID": iD, "Licence Plate": textLP, "Registration Date": regis_date, "Expiration Date": expired_date}
    manager_collection.insert_one(db)

    return db


class ADD(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("addLP.ui", self)

        self.btnOK.clicked.connect(self.addNew)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def addNew(self):
        self.message = QMessageBox()
        textLP = self.txtLP.toPlainText()
        iD = self.txtID.toPlainText()
        if textLP == "" or iD == "":
            self.message.setWindowTitle("Message")
            self.message.setText("Error")
            self.message.setIcon(QMessageBox.Warning)
            self.message.exec_()
        else:
            self.message.setWindowTitle("Message")
            self.message.setText("OK")
            self.message.setIcon(QMessageBox.Information)
            self.message.exec_()
