# from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QLineEdit, QApplication
# from PyQt5 import uic
# from PyQt5.QtCore import pyqtSignal

# from pymongo import MongoClient
# cluster = "mongodb://10.37.239.135:27017"
# client = MongoClient(cluster)
# db = client.lpr
# user_collection = db.user_collection


# from main import MAIN
# from addMonth import ADDMONTH
# from deleteLP import DELETE
# from addDay import ADDDAY
# from checkList import CHECKLIST

# class LOGIN(QMainWindow):
#     loggedSignal = pyqtSignal()
#     def __init__(self):
#         super().__init__()
#         uic.loadUi("login.ui", self)
#         self.LOG_IN = False
#         # self.show()
#         self.txtPassword.setEchoMode(QLineEdit.EchoMode.Password)
#         self.btnLogin.clicked.connect(self.loginFunction)

#     def center(self):
#         qr = self.frameGeometry()
#         cp = QDesktopWidget().availableGeometry().center()
#         qr.moveCenter(cp)
#         self.move(qr.topLeft())

#     def loginFunction(self):
#         user = self.txtUser.text()
#         password = self.txtPassword.text()

#         if len(user) == 0 or len(password) == 0:
#             self.lblError.setText("Please input all fields")
#             self.LOG_IN = False
#         else:
#             document = user_collection.find_one({"user": user})
#             if document is None:
#                 self.lblError.setText("User does not exist")
#                 self.LOG_IN = False
#             else:
#                 resultPassword = list(document.values())[2]
#                 if resultPassword == password:
#                     self.lblError.setText("")
#                     self.LOG_IN = True
#                 else:
#                     self.lblError.setText("Invalid Password")
#                     self.LOG_IN = False
#         if self.LOG_IN:
#             self.loggedSignal.emit()
#         else:
#             QApplication.quit()
#         self.close()


# class UI():
#     def __init__(self):
#         self.main = MAIN()
#         self.main.show()

#         # self.main.center()
#         self.main.btnAddMonth.clicked.connect(lambda: self.ChangeUI("addMonth"))
#         self.main.btnAddDay.clicked.connect(lambda: self.ChangeUI("addDay"))
#         self.main.btnDelete.clicked.connect(lambda: self.ChangeUI("deleteLP"))
#         self.main.btnCheckList.clicked.connect(lambda: self.ChangeUI("checkList"))

#         self.addMonth = ADDMONTH()
#         self.addMonth.btnOK.clicked.connect(self.addMonth.addNew)
#         self.addMonth.btnCancel.clicked.connect(lambda: self.ChangeUI("main"))

#         self.addDay = ADDDAY()
#         self.addDay.btnOK.clicked.connect(self.addDay.addNew)
#         self.addDay.btnCancel.clicked.connect(lambda: self.ChangeUI("main"))

#         self.deleteLP = DELETE()
#         self.deleteLP.btnOK.clicked.connect(self.deleteLP.detele)
#         self.deleteLP.btnCancel.clicked.connect(lambda: self.ChangeUI("main"))

#         self.checkList = CHECKLIST()
#         self.checkList.btnCancel.clicked.connect(lambda: self.ChangeUI("main"))

#     def ChangeUI(self, i):
#         if i == "addMonth":
#             self.main.hide()
#             # self.addLP.center()
#             self.addMonth.show()
#         elif i == "addDay":
#             self.main.hide()
#             self.addDay.show()
#         elif i == "deleteLP":
#             self.main.hide()
#             # self.deleteLP.center()
#             self.deleteLP.show()
#         elif i == "checkList":
#             self.main.hide()
#             # self.checkList.center()
#             self.checkList.show()
#         elif i == "main":
#             self.addMonth.hide()
#             self.addDay.hide()
#             self.deleteLP.hide()
#             self.checkList.hide()
#             # self.main.center()
#             self.main.show()


# if __name__ == "__main__":
#     app = QApplication([])
#     login = LOGIN()
#     ui = UI()
#     login.loggedSignal.connect(ui)
#     app.exec_()