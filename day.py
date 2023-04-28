from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication, QSlider, QHeaderView, QTableWidgetItem
from PyQt5 import uic

from pymongo import MongoClient
cluster = "mongodb+srv://tuyennt:0711@lpr.3u3tc8j.mongodb.net/test"
client = MongoClient(cluster)
db = client.lpr
priceData = db.price

def add2Price(vehicle, name, nightStart, nightEnd, dayPrice, nightPrice, monthPrice, addPrice, addStart, addEnd):
    db = {"Loại phương tiện": vehicle, "Tên": name, "Bắt đầu đêm": nightStart, "Kết thúc đêm": nightEnd, "Giá ngày": dayPrice, "Giá đêm": nightPrice,
           "Giá vé tháng": monthPrice, "Giá phụ thu": addPrice, "Bắt đầu phụ thu": addStart, "Kết thúc phụ thu": addEnd, "Trạng thái": "Chưa sử dụng"}
    
    priceData.insert_one(db)

def update2Price(id, vehicle, name, nightStart, nightEnd, dayPrice, nightPrice, monthPrice, addPrice, addStart, addEnd):
    priceData.find_one_and_update({"_id": id}, {"$set": {"Loại phương tiện": vehicle, "Tên": name, "Bắt đầu đêm": nightStart, "Kết thúc đêm": nightEnd, "Giá ngày": dayPrice, "Giá đêm": nightPrice,
                                    "Giá vé tháng": monthPrice, "Giá phụ thu": addPrice, "Bắt đầu phụ thu": addStart, "Kết thúc phụ thu": addEnd}})
    
def checkName(name):
    check = priceData.find_one({"Tên": name})

    return check


class DAY(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Day.ui", self)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.sld1.valueChanged.connect(self.slideIt1)
        self.sld1.setTickInterval(5)
        self.sld1.setTickPosition(QSlider.TicksBothSides)

        self.sld2.valueChanged.connect(self.slideIt2)
        self.sld2.setTickInterval(5)
        self.sld2.setTickPosition(QSlider.TicksBothSides)

        self.sld3.valueChanged.connect(self.slideIt3)
        self.sld3.setTickInterval(5)
        self.sld3.setTickPosition(QSlider.TicksBothSides)

        self.sld4.valueChanged.connect(self.slideIt4)
        self.sld4.setTickInterval(5)
        self.sld4.setTickPosition(QSlider.TicksBothSides)

        self.btnOK.clicked.connect(self.addNew)
        self.btnUpdate.clicked.connect(self.displayUpdate)
        self.btnOKUpdate.clicked.connect(self.update)
        self.btnDelete.clicked.connect(self.delete)
        self.btnCancel.clicked.connect(self.cancel)
        self.btnUse.clicked.connect(self.use)

        self.btnOKUpdate.setEnabled(False)

        self.id = ""

        self.displayTable()
        # self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def slideIt1(self, value):
        self.lnSld1.setText(str(value))

    def slideIt2(self, value):
        self.lnSld2.setText(str(value))

    def slideIt3(self, value):
        self.lnSld3.setText(str(value))

    def slideIt4(self, value):
        self.lnSld4.setText(str(value))

    def displayTable(self):
        self.table.setRowCount(0)
        for data in priceData.find({}):
            self.table.insertRow(0)
            self.table.setItem(0, 0, QTableWidgetItem(data["Tên"]))
            self.table.setItem(0, 1, QTableWidgetItem(data["Loại phương tiện"]))
            self.table.setItem(0, 2, QTableWidgetItem(data["Trạng thái"]))

    def addNew(self):
        self.lblMessage.setText("")
        vehicle = self.cbbVehicle.currentText()
        name = self.lnName.text()
        nightStart = self.lnSld1.text()
        nightEnd = self.lnSld2.text()
        dayPrice = self.spb1.value()
        nightPrice = self.spb2.value()
        monthPrice = self.spb3.value()
        addPrice = self.spb4.value()
        addStart = self.lnSld3.text() 
        addEnd = self.lnSld4.text()

        check = checkName(name)

        if name == "":
            self.lblMessage.setText("NHẬP TÊN CÔNG THỨC")
        elif check is not None:
            self.lblMessage.setText("TÊN CÔNG THỨC ĐÃ TỒN TẠI")
        else:
            add2Price(vehicle, name, nightStart, nightEnd, dayPrice, nightPrice, monthPrice, addPrice, addStart, addEnd)
            self.lblMessage.setText("THÊM CÔNG THỨC THÀNH CÔNG")
        
        self.displayTable()

    def delete(self):
        self.lblMessage.setText("")
        selected = self.table.selectionModel().selectedRows()
        if selected:
            row = selected[0].row()
            name = self.table.item(row, 0).text()
            priceData.delete_one({"Tên": name})
            self.table.removeRow(row)

        self.displayTable()

    def displayUpdate(self):
        self.lblMessage.setText("")
        selected = self.table.selectionModel().selectedRows()
        if selected:
            self.btnOK.setEnabled(False)
            self.btnOKUpdate.setEnabled(True)

            row = selected[0].row()
            name = self.table.item(row, 0).text()
            data = priceData.find_one({"Tên": name})
            if data:
                self.id = data["_id"]
                self.cbbVehicle.setCurrentText(data["Loại phương tiện"])
                self.lnName.setText(data["Tên"])
                self.sld1.setValue(int(data["Bắt đầu đêm"]))
                self.lnSld1.setText(data["Bắt đầu đêm"])
                self.sld2.setValue(int(data["Kết thúc đêm"]))
                self.lnSld2.setText(data["Kết thúc đêm"])
                self.spb1.setValue(data["Giá ngày"])
                self.spb2.setValue(data["Giá đêm"])
                self.spb3.setValue(data["Giá vé tháng"])
                self.spb4.setValue(data["Giá phụ thu"])
                self.sld3.setValue(int(data["Bắt đầu phụ thu"]))
                self.lnSld3.setText(data["Bắt đầu phụ thu"])
                self.sld4.setValue(int(data["Kết thúc phụ thu"]))
                self.lnSld4.setText(data["Kết thúc phụ thu"])

    def update(self):
        vehicle = self.cbbVehicle.currentText()
        name = self.lnName.text()
        nightStart = self.lnSld1.text()
        nightEnd = self.lnSld2.text()
        dayPrice = self.spb1.value()
        nightPrice = self.spb2.value()
        monthPrice = self.spb3.value()
        addPrice = self.spb4.value()
        addStart = self.lnSld3.text()
        addEnd = self.lnSld4.text()

        if name == "":
            self.lblMessage.setText("NHẬP TÊN CÔNG THỨC")
        else:
            update2Price(self.id, vehicle, name, nightStart, nightEnd, dayPrice, nightPrice, monthPrice, addPrice, addStart, addEnd)
            self.lblMessage.setText("SỬA CÔNG THỨC THÀNH CÔNG")

            self.btnOK.setEnabled(True)
            self.btnOKUpdate.setEnabled(False)

            # self.cbbVehicle.setItemText()
            self.lnName.setText("")
            self.sld1.setValue(0)
            self.lnSld1.setText("0")
            self.sld2.setValue(0)
            self.lnSld2.setText("0")
            self.spb1.setValue(0)
            self.spb2.setValue(0)
            self.spb3.setValue(0)
            self.spb4.setValue(0)
            self.sld3.setValue(0)
            self.lnSld3.setText("0")
            self.sld4.setValue(0)
            self.lnSld4.setText("0")
        
        self.displayTable()

    def cancel(self):
        self.btnOK.setEnabled(True)
        self.btnOKUpdate.setEnabled(False)

        self.lnName.setText("")
        self.sld1.setValue(0)
        self.lnSld1.setText("0")
        self.sld2.setValue(0)
        self.lnSld2.setText("0")
        self.spb1.setValue(0)
        self.spb2.setValue(0)
        self.spb3.setValue(0)
        self.spb4.setValue(0)
        self.sld3.setValue(0)
        self.lnSld3.setText("0")
        self.sld4.setValue(0)
        self.lnSld4.setText("0")

    def use(self):
        selected = self.table.selectionModel().selectedRows()
        if selected:
            row = selected[0].row()
            name = self.table.item(row, 0).text()
            vehicle = self.table.item(row, 1).text()
            priceData.update_many({"Loại phương tiện": vehicle}, {"$set": {"Trạng thái": "Chưa sử dụng"}})
            priceData.update_one({"Tên": name}, {"$set": {"Trạng thái": "Sử dụng"}})

        self.displayTable()
            