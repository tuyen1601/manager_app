from PyQt5.QtWidgets import QMainWindow, QDesktopWidget
from PyQt5 import uic

class ADDCARD(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("addCard.ui", self)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())