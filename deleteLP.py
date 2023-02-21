from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QMessageBox
from PyQt5 import uic

from pymongo import MongoClient
cluster = "mongodb://localhost:27017"
client = MongoClient(cluster)
db = client.lpr
manager_collection = db.manager_collection

def delete2Manager(content, text):
    if content == "ID":
        status = manager_collection.find_one_and_delete({"ID": text})
        if status is None:
            message_warning()
        else:
            message_information()
    else:
        status = manager_collection.find_one_and_delete({"Licence Plate": text})
        if status is None:
            message_warning()
        else:
            message_information()


def message_warning():
    message = QMessageBox()
    message.setWindowTitle("Message")
    message.setText("Does Not Exist")
    message.setIcon(QMessageBox.Warning)
    message.exec_()

def message_information():
    message = QMessageBox()
    message.setWindowTitle("Message")
    message.setText("OK")
    message.setIcon(QMessageBox.Information)
    message.exec_()


class DELETE(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("deleteLP.ui", self)

        self.btnOK.clicked.connect(self.detele)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def detele(self):
        content = self.cbb.currentText()
        text = self.txt.toPlainText()
        delete2Manager(content, text)
        self.txt.clear()

        