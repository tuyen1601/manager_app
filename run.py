from PyQt5.QtWidgets import QApplication

from main import MAIN
from addLP import ADD
from deleteLP import DELETE

class UI():
    def __init__(self):
        self.main = MAIN()
        self.main.center()
        self.main.show()

        self.main.btnAdd.clicked.connect(lambda: self.ChangeUI("addLP"))
        self.main.btnDelete.clicked.connect(lambda: self.ChangeUI("deleteLP"))

        self.addLP = ADD()
        self.addLP.btnCancelAdd.clicked.connect(lambda: self.ChangeUI("main"))

        self.deleteLP = DELETE()
        self.deleteLP.btnCancelDelete.clicked.connect(lambda: self.ChangeUI("main"))

    def ChangeUI(self, i):
        if i == "addLP":
            self.main.hide()
            self.addLP.center()
            self.addLP.show()
        elif i == "deleteLP":
            self.main.hide()
            self.deleteLP.center()
            self.deleteLP.show()
        elif i == "main":
            self.addLP.hide()
            self.deleteLP.hide()
            self.main.center()
            self.main.show()


if __name__ == "__main__":
    app = QApplication([])
    ui = UI()
    app.exec_()