from newtransaction import Ui_Dialog
from PySide2.QtWidgets import QDialog, QApplication
from PySide2.QtCore import Signal, Slot
import sqlite3
from datetime import datetime


class transactionDialog(QDialog):
    
    dataready = Signal(object)
    depSelected = Signal(str)

    def __init__(self):
        super().__init__()
        self.data = {}
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.accepted.connect(self.makedict)
        self.loadDepList()
        self.ui.comboBox.currentIndexChanged.connect(self.loadEmpList)
    
    def loadDepList(self):
        with sqlite3.connect('test2.db') as conn:
            departments = conn.execute('select * from departments')
        self.departments = [dep[0] for dep in departments.fetchall()]
        self.ui.comboBox.addItems(self.departments)

    @Slot()
    def loadEmpList(self):
        self.ui.listWidget.clear()
        department = self.ui.comboBox.currentText()
        with sqlite3.connect('test2.db') as conn:
            employees = conn.execute('select empid, "empname" from employees where department = :dept',{'dept':department})
        self.employees = {emp[1]:emp[0] for emp in employees.fetchall()}
        self.ui.listWidget.addItems(list(self.employees.keys()))
        
    def makedict(self):
        date = datetime.strptime(self.ui.dateEdit.text(), '%d-%b-%y')
        date = datetime.strftime(date,'%Y-%m-%d')
        department = self.ui.comboBox.currentText()
        try:
            empid = self.employees[self.ui.listWidget.currentItem().text()]
        except:
            pass
        
        amount = self.ui.lineEdit_2.text()
        self.data = {'date':date, 'department':department, 'empid':empid, 'amount':amount}
        self.dataready.emit(self.data)
        




