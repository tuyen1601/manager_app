from PyQt5.QtWidgets import QApplication

from main import MAIN
from addMonth import addMonth
from deleteLP import DELETE
from addDay import addDay
from checkList import CHECKLIST

class UI():
    def __init__(self):
        self.main = MAIN()
        # self.main.center()
        self.main.show()

        self.main.btnAddMonth.clicked.connect(lambda: self.ChangeUI("addMonth"))
        self.main.btnAddDay.clicked.connect(lambda: self.ChangeUI("addDay"))
        self.main.btnDelete.clicked.connect(lambda: self.ChangeUI("deleteLP"))
        self.main.btnCheckList.clicked.connect(lambda: self.ChangeUI("checkList"))

        self.addMonth = addMonth()
        self.addMonth.btnCancelMonth.clicked.connect(lambda: self.ChangeUI("main"))

        self.addDay = addDay()
        self.addDay.btnCancelDay.clicked.connect(lambda: self.ChangeUI("main"))

        self.deleteLP = DELETE()
        self.deleteLP.btnCancelDelete.clicked.connect(lambda: self.ChangeUI("main"))

        self.checkList = CHECKLIST()
        self.checkList.btnCancelList.clicked.connect(lambda: self.ChangeUI("main"))

    def ChangeUI(self, i):
        if i == "addMonth":
            self.main.hide()
            # self.addLP.center()
            self.addMonth.show()
        elif i == "addDay":
            self.main.hide()
            self.addDay.show()
        elif i == "deleteLP":
            self.main.hide()
            # self.deleteLP.center()
            self.deleteLP.show()
        elif i == "checkList":
            self.main.hide()
            # self.checkList.center()
            self.checkList.show()
        elif i == "main":
            self.addMonth.hide()
            self.addDay.hide()
            self.deleteLP.hide()
            self.checkList.hide()
            # self.main.center()
            self.main.show()


if __name__ == "__main__":
    app = QApplication([])
    ui = UI()
    app.exec_()