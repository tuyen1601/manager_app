from datetime import datetime

from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QHeaderView, QTableWidgetItem, QApplication, QFileDialog, QMessageBox
from PyQt5 import uic

from addMonth import ADDMONTH
from pymongo import MongoClient

import pandas as pd

cluster = "mongodb+srv://tuyennt:0711@lpr.3u3tc8j.mongodb.net/test"
client = MongoClient(cluster)
db = client.lpr
manager_collection = db.manager_collection
card = db.card
price_collection = db.price

def updateDate2Manager(iD, regisDate, expiredDate):
    manager_collection.find_one_and_update({"Mã thẻ": iD}, {"$set": {"Ngày đăng ký": regisDate, "Ngày hết hạn": expiredDate}})

def updateID2Manager(plate, id):
    manager_collection.find_one_and_update({"Biển số": plate}, {"$set": {"Mã thẻ": id}})

def add2Manager(name, address, textLP, vehicle, id, regisDate, expiredDate, model, phone, price, note):
    db = {"Mã thẻ": id, "Chủ xe": name, "Địa chỉ": address, "Biển số": textLP, "Loại xe": vehicle, "Ngày đăng ký": regisDate, 
          "Ngày hết hạn": expiredDate, "Nhãn hiệu": model, "Điện thoại": phone, "Giá vé": price, "Loại vé": "Vé tháng", "Ghi chú": note}
    manager_collection.insert_one(db)

def checkID(id):
    return card.find_one({"Mã thẻ": id})

############################ begin

def updateStatus_LP_ByID(id, status, textLP):
    card.find_one_and_update({"Mã thẻ": id}, {"$set": {"Trạng thái": status, "Biển số": textLP}})

def checkLP(textLP):
    return manager_collection.find_one({"Biển số": textLP})

############################ end

def messageCheckRegis(success_count, sum_count):
    message = QMessageBox()
    message.setWindowTitle("Message")
    message.setText("Đã thêm thành công {}/{} thẻ".format(success_count, sum_count))
    message.setIcon(QMessageBox.Information)
    message.exec_()

class MONTH(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Month.ui", self)

        self.tableMonth.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        #display row
        self.displayList()

        #search 
        self.lnSearch.textChanged.connect(self.search)

        #delete row
        self.btnDelete.clicked.connect(self.removeRow)

        self.addMonth = ADDMONTH()

        #update date
        self.btnUpdate.clicked.connect(self.displayUpdateDate)
        self.addMonth.btnUpdateDate.clicked.connect(self.updateDate)

        #change card
        self.btnChange.clicked.connect(self.displayUpdateID)
        self.addMonth.btnChange.clicked.connect(self.updateID)

        #add new
        self.btnAdd.clicked.connect(self.displayAddNew)
        self.addMonth.btnRandom.clicked.connect(self.randomID)
        # self.btnAdd.clicked.connect(self.addMonth.lblMessage.setText(""))
        self.addMonth.btnOK.clicked.connect(self.addNew)

        #refresh table
        self.btnRefresh.clicked.connect(self.displayList)

        self.addMonth.btnCancel.clicked.connect(lambda: self.changUI("checkList"))

########################################################## begin

        #import excel
        self.btnImport.clicked.connect(self.showSelectedOpenFile)

    def showSelectedOpenFile(self):
        fname = QFileDialog.getOpenFileName(self, "Open File", "", "Excel Files (*xlsx)")

        if fname[0]:
            success_count = 0
            lp_duplicate_count = 0

            self.lblSelectedFile.setText(fname[0])
            df = pd.read_excel(fname[0], sheet_name='Sheet1')
            df['Trạng thái thêm'] = 'Thêm thành công'
            
            for index, row in df.iterrows():
                excel_name = row[0]
                excel_address = row[1]  
                excel_textLP = row[2]  
                excel_vehicle = row[3]  
                excel_regisDate = row[4].strftime('%d %m %Y')  
                excel_expiredDate = row[5].strftime('%d %m %Y')  
                excel_model = row[6]  
                excel_phone = str(row[7])  
                excel_category = row[8]
                excel_note = str(row[9])

                if checkLP(excel_textLP) != None:
                    df.iloc[index, 10] = "Xe đã được đăng ký trước đó"
                    lp_duplicate_count += 1
                else:
                    search_command = {"Loại thẻ": "Thẻ tháng", "Trạng thái": "Chưa sử dụng"}
                    if card.count_documents(search_command) == 0:
                        df.iloc[index, 10] = "Xe chưa được đăng ký do thiếu thẻ trống"
                    else:
                        random_id = card.find_one(search_command)["Mã thẻ"]
                        if price_collection.count_documents({}) == 0:
                            priceVehicle = 0 
                        else:
                            priceVehicle = price_collection.find_one({"Loại phương tiện": excel_vehicle, "Trạng thái": "Sử dụng"})["Giá vé tháng"]
                        add2Manager(excel_name, excel_address, excel_textLP, excel_vehicle, random_id, 
                                    excel_regisDate, excel_expiredDate, excel_model, excel_phone, priceVehicle, excel_note)
                        updateStatus_LP_ByID(random_id, status="Đã sử dụng", textLP=excel_textLP)
                        success_count += 1
            
            sum_count = df.shape[0]
            messageCheckRegis(success_count, sum_count)

            self.displayList()
            df.to_excel('output.xlsx', index=False)

########################################################## end

    def randomID(self):
        search_command = {"Loại thẻ": "Thẻ tháng", "Trạng thái": "Chưa sử dụng"}
        if card.count_documents(search_command) == 0:
            self.addMonth.lblMessage.setText("Hết thẻ trống")
        else:
            idRandom = card.find_one(search_command)["Mã thẻ"]
            self.addMonth.txtID.setText(idRandom)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def changUI(self, i):
        if i == "checkList":
            self.addMonth.hide()

    def displayList(self):
        self.tableMonth.setRowCount(0)
        for data in manager_collection.find({}):
            self.tableMonth.insertRow(0)
            self.tableMonth.setItem(0, 0, QTableWidgetItem(data["Mã thẻ"]))
            self.tableMonth.setItem(0, 1, QTableWidgetItem(data["Biển số"]))
            self.tableMonth.setItem(0, 2, QTableWidgetItem(data["Chủ xe"]))
            self.tableMonth.setItem(0, 3, QTableWidgetItem(data["Ngày đăng ký"]))
            self.tableMonth.setItem(0, 4, QTableWidgetItem(data["Ngày hết hạn"]))
            self.tableMonth.setItem(0, 5, QTableWidgetItem(data["Loại xe"]))
            self.tableMonth.setItem(0, 6, QTableWidgetItem(str(data["Giá vé"])))
            #check time 
            objDateRegis = datetime.strptime(data["Ngày đăng ký"], "%d %m %Y")
            objDateExpired = datetime.strptime(data["Ngày hết hạn"], "%d %m %Y")
            dateNow = datetime.now()
            if dateNow >= objDateRegis and dateNow <= objDateExpired:
                self.tableMonth.setItem(0, 7, QTableWidgetItem("Chưa hết hạn"))
            else:
                self.tableMonth.setItem(0, 7, QTableWidgetItem("Hết hạn"))
            
    def search(self):
        content = self.cbbSearch.currentText()
        strSearch = self.lnSearch.text().lower()
        for row in range(self.tableMonth.rowCount()):
            if content == "Mã thẻ":
                item = self.tableMonth.item(row, 0)
            if content == "Biển số":
                item = self.tableMonth.item(row, 1)
            if item is not None:
                self.tableMonth.setRowHidden(row, strSearch not in item.text().lower())
            else:
                self.tableMonth.setRowHidden(row, True)

    def removeRow(self):
        selectedMonth = self.tableMonth.selectionModel().selectedRows()
        if selectedMonth:
            for i in range(len(selectedMonth)):
                row = selectedMonth[0].row()
                iD = self.tableMonth.item(row, 0).text()
                manager_collection.delete_one({"Mã thẻ": iD})
                card.find_one_and_update({"Mã thẻ": iD}, {"$set": {"Trạng thái": "Chưa sử dụng", "Biển số": ""}})
                self.tableMonth.removeRow(row)
                i += 1

    def displayAddNew(self):
        self.addMonth.btnChange.setEnabled(False)
        self.addMonth.btnUpdateDate.setEnabled(False)
        self.addMonth.btnOK.setEnabled(True)

        self.addMonth.dateRegis.setDate(datetime.now().date())
        self.addMonth.dateExpired.setDate(datetime.now().date())

        self.addMonth.txtName.clear()
        self.addMonth.txtAddress.clear()
        self.addMonth.txtPhone.clear()
        self.addMonth.txtModel.clear()
        self.addMonth.txtLP.clear()
        self.addMonth.txtID.clear()
        self.addMonth.spbPrice.setValue(0)

        self.addMonth.lblName.setText("")
        self.addMonth.lblAddress.setText("")
        self.addMonth.lblLP.setText("")
        self.addMonth.lblID.setText("")
        self.addMonth.lblDate.setText("")
        self.addMonth.lblPhone.setText("")
        self.addMonth.lblModel.setText("")
        self.addMonth.txtNote.setText("")

        self.addMonth.dateRegis.setEnabled(True)
        self.addMonth.dateExpired.setEnabled(True)
        self.addMonth.txtID.setEnabled(True)
        self.addMonth.txtLP.setEnabled(True)
        self.addMonth.txtName.setEnabled(True)
        self.addMonth.txtAddress.setEnabled(True) 
        self.addMonth.txtPhone.setEnabled(True)
        self.addMonth.txtModel.setEnabled(True)
        self.addMonth.txtLP.setEnabled(True)
        self.addMonth.cbbVehicle.setEnabled(True)
        self.addMonth.spbPrice.setEnabled(True)

        self.addMonth.show()

    def addNew(self):
        name = self.addMonth.txtName.text().upper()
        address = self.addMonth.txtAddress.text().upper()
        textLP = self.addMonth.txtLP.text().upper()
        vehicle = self.addMonth.cbbVehicle.currentText()
        id = self.addMonth.txtID.text().upper()
        regisDate = self.addMonth.dateRegis.text()
        expiredDate = self.addMonth.dateExpired.text()
        model = self.addMonth.txtModel.text().upper()
        phone = self.addMonth.txtPhone.text()
        price = self.addMonth.spbPrice.value()
        note = self.addMonth.txtNote.text()

        self.addMonth.lblMessage.setText("")
        if name == "" or address == "" or textLP == "" or id == "" or regisDate >= expiredDate or phone == "" or model == "":
            if name == "":
                self.addMonth.lblName.setText("Nhập họ tên chủ xe")
            else:
                self.addMonth.lblName.setText("")
            if address == "":
                self.addMonth.lblAddress.setText("Nhập địa chỉ chủ xe")
            else:
                self.addMonth.lblAddress.setText("")
            if textLP == "":
                self.addMonth.lblLP.setText("Nhập biển số xe")
            else:
                self.addMonth.lblLP.setText("")
            if id == "":
                self.addMonth.lblID.setText("Nhập mã thẻ")
            else:
                self.addMonth.lblID.setText("")
            if regisDate >= expiredDate:
                self.addMonth.lblDate.setText("Sai ngày đăng ký")
            else:
                self.addMonth.lblDate.setText("")
            if phone == "":
                self.addMonth.lblPhone.setText("Nhập số điện thoại")
            else:
                self.addMonth.lblPhone.setText("")
            if model == "":
                self.addMonth.lblModel.setText("Nhập nhãn hiệu xe")
            else:
                self.addMonth.lblModel.setText("")
        else:
            doc = checkID(id)
            if doc is not None:
                if doc["Trạng thái"] == "Chưa sử dụng":
                    self.addMonth.lblMessage.setText("ĐĂNG KÝ THÀNH CÔNG")
                    add2Manager(name, address, textLP, vehicle, id, regisDate, expiredDate, model, phone, price, note)
                    updateStatus_LP_ByID(id, status="Đã sử dụng", textLP=textLP)
                    self.addMonth.txtName.clear()
                    self.addMonth.txtAddress.clear()
                    self.addMonth.txtPhone.clear()
                    self.addMonth.txtModel.clear()
                    self.addMonth.txtLP.clear()
                    self.addMonth.txtID.clear()

                    self.addMonth.lblName.setText("")
                    self.addMonth.lblAddress.setText("")
                    self.addMonth.lblLP.setText("")
                    self.addMonth.lblID.setText("")
                    self.addMonth.lblDate.setText("")
                    self.addMonth.lblPhone.setText("")
                    self.addMonth.lblModel.setText("")
                else:
                    self.addMonth.lblID.setText("Thẻ đã tồn tại")
            else:
                self.addMonth.lblID.setText("Thẻ không tồn tại")
                
        self.displayList()

    def displayUpdate(self, data):
        self.addMonth.lblMessage.setText("")
        self.addMonth.lblDate.setText("")

        self.addMonth.lblName.setText("")
        self.addMonth.lblAddress.setText("")
        self.addMonth.lblLP.setText("")
        self.addMonth.lblID.setText("")
        self.addMonth.lblDate.setText("")
        self.addMonth.lblPhone.setText("")
        self.addMonth.lblModel.setText("")

        if data:
            id = data["Mã thẻ"]
            plate = data["Biển số"]
            name =  data["Chủ xe"]
            address = data["Địa chỉ"]
            vehicle = data["Loại xe"]
            regis = data["Ngày đăng ký"]
            expired = data["Ngày hết hạn"]
            phone = data["Điện thoại"]
            model = data["Nhãn hiệu"]
            note = data["Ghi chú"]
            price = data["Giá vé"]
            objDateRegis = datetime.strptime(regis, "%d %m %Y")
            objDateExpired = datetime.strptime(expired, "%d %m %Y")

            self.addMonth.show()
            self.addMonth.txtID.setText(id)
            self.addMonth.txtLP.setText(plate)
            self.addMonth.txtName.setText(name)
            self.addMonth.txtAddress.setText(address)
            self.addMonth.cbbVehicle.setCurrentText(vehicle)
            self.addMonth.txtPhone.setText(phone)
            self.addMonth.txtModel.setText(model)
            self.addMonth.txtNote.setText(note)
            self.addMonth.dateRegis.setDate(objDateRegis)
            self.addMonth.dateExpired.setDate(objDateExpired)
            self.addMonth.spbPrice.setValue(price)
    
    def displayUpdateDate(self):
        self.addMonth.btnOK.setEnabled(False)
        self.addMonth.btnChange.setEnabled(False)
        self.addMonth.btnUpdateDate.setEnabled(True)

        selectedMonth = self.tableMonth.selectionModel().selectedRows()
        if selectedMonth:
            row = selectedMonth[0].row()
            id = self.tableMonth.item(row, 0).text()
            data = manager_collection.find_one({"Mã thẻ": id})

            self.displayUpdate(data)
            self.addMonth.dateRegis.setEnabled(True)
            self.addMonth.dateExpired.setEnabled(True)
            self.addMonth.txtID.setEnabled(False)
            self.addMonth.txtLP.setEnabled(False)
            self.addMonth.txtName.setEnabled(False)
            self.addMonth.txtAddress.setEnabled(False) 
            self.addMonth.txtPhone.setEnabled(False)
            self.addMonth.txtModel.setEnabled(False)
            self.addMonth.txtLP.setEnabled(False)
            self.addMonth.cbbVehicle.setEnabled(False)
            self.addMonth.spbPrice.setEnabled(False)
    
    def updateDate(self):
        id = self.addMonth.txtID.text()
        regisDate = self.addMonth.dateRegis.text()
        expiredDate = self.addMonth.dateExpired.text()

        objDateRegis = datetime.strptime(regisDate, "%d %m %Y")
        objDateExpired = datetime.strptime(expiredDate, "%d %m %Y")
        dateNow = datetime.now()
        if dateNow >= objDateRegis and dateNow <= objDateExpired:
            updateDate2Manager(id, regisDate, expiredDate)
            self.addMonth.lblMessage.setText("GIA HẠN THÀNH CÔNG")
        else:
            self.addMonth.lblDate.setText("Ngày tháng không hợp lệ")

        self.displayList()
        
    def displayUpdateID(self):
        self.addMonth.btnOK.setEnabled(False)
        self.addMonth.btnUpdateDate.setEnabled(False)
        self.addMonth.btnChange.setEnabled(True)

        selectedMonth = self.tableMonth.selectionModel().selectedRows()
        if selectedMonth:
            row = selectedMonth[0].row()
            id = self.tableMonth.item(row, 0).text()
            data = manager_collection.find_one({"Mã thẻ": id})

            self.displayUpdate(data)
            self.addMonth.txtID.setEnabled(True)
            self.addMonth.txtLP.setEnabled(False)
            self.addMonth.txtName.setEnabled(False)
            self.addMonth.txtAddress.setEnabled(False) 
            self.addMonth.txtPhone.setEnabled(False)
            self.addMonth.txtModel.setEnabled(False)
            self.addMonth.txtLP.setEnabled(False)
            self.addMonth.cbbVehicle.setEnabled(False)
            self.addMonth.spbPrice.setEnabled(False)
            self.addMonth.dateRegis.setEnabled(False)
            self.addMonth.dateExpired.setEnabled(False)

    def updateID(self):
        id = self.addMonth.txtID.text()
        plate = self.addMonth.txtLP.text()

        doc = checkID(id)
        if doc is not None:
            if doc["Trạng thái"] == "Chưa sử dụng":
                updateID2Manager(plate, id)
                self.addMonth.lblMessage.setText("ĐỔI THẺ THÀNH CÔNG")
            else:
                self.addMonth.lblMessage.setText("THẺ ĐANG ĐƯỢC SỬ DỤNG")
                self.addMonth.lblMessage.setStyleSheet("color: red")
        else:
            self.addMonth.lblMessage.setText("THẺ KHÔNG TỒN TẠI")
            self.addMonth.lblMessage.setStyleSheet("color: red")
        self.displayList()


if __name__ == "__main__":
    app = QApplication([])
    a = MONTH()
    a.show()
    app.exec_()
