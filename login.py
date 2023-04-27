from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QLineEdit, QApplication
from PyQt5 import uic

from menu import MENU

from pymongo import MongoClient
cluster = "mongodb+srv://tuyennt:0711@lpr.3u3tc8j.mongodb.net/test"
client = MongoClient(cluster)
db = client.lpr
user_collection = db.user_collection


class LOGIN(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("login.ui", self)

        self.menu = MENU()

        self.show()
        self.txtPassword.setEchoMode(QLineEdit.EchoMode.Password)
        self.btnLogin.clicked.connect(self.loginFunction)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def loginFunction(self):
        user = self.txtUser.text()
        password = self.txtPassword.text()

        if len(user) == 0 or len(password) == 0:
            self.lblError.setText("Please input all fields")
        else:
            document = user_collection.find_one({"user": user})
            if document is None:
                self.lblError.setText("User does not exist")
            else:
                resultPassword = list(document.values())[2]
                if resultPassword == password:
                    self.lblError.setText("")
                    self.hide()
                    self.menu.show()
                else:
                    self.lblError.setText("Invalid Password")


if __name__ == "__main__":
    app = QApplication([])
    login = LOGIN()
    app.exec()