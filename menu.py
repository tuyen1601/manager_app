from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication
from PyQt5 import uic

from month import MONTH
from day import DAY
from vehicleLookup import LOOKUP
from revenue import REVENUE
from card import CARD

class MENU(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("menu.ui", self)

        self.show()

        self.btnMonth.clicked.connect(lambda: self.changUI("month"))
        self.btnDay.clicked.connect(lambda: self.changUI("day"))
        self.btnlookUp.clicked.connect(lambda: self.changUI("lookup"))
        self.btnRevenue.clicked.connect(lambda: self.changUI("revenue"))
        self.btnCard.clicked.connect(lambda: self.changUI("card"))

        self.month = MONTH()
        self.month.btnBack.clicked.connect(lambda: self.changUI("menu"))
        self.btnMonth.clicked.connect(self.month.displayList)

        self.day = DAY()
        self.day.btnBack.clicked.connect(lambda: self.changUI("menu"))

        self.lookUp = LOOKUP()
        self.lookUp.btnBack.clicked.connect(lambda: self.changUI("menu"))
        self.btnlookUp.clicked.connect(self.lookUp.displayTable)

        self.revenue = REVENUE()
        self.revenue.btnBack.clicked.connect(lambda: self.changUI("menu"))

        self.card = CARD()
        self.card.btnBack.clicked.connect(lambda: self.changUI("menu"))
        self.btnCard.clicked.connect(self.card.displayTable)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def changUI(self, i):
        if i == "month":
            self.hide()
            self.month.show()
        elif i == "day":
            self.hide()
            self.day.show()
        elif i == "lookup":
            self.hide()
            self.lookUp.show()
        elif i == "revenue":
            self.hide()
            self.revenue.show()
        elif i == "card":
            self.hide()
            self.card.show()
        elif i == "menu":
            self.show()
            self.month.hide()
            self.day.hide()
            self.lookUp.hide()
            self.revenue.hide()
            self.card.hide()

if __name__ == "__main__":
    app = QApplication([])
    menu = MENU()
    app.exec()