import newtransaction
import displaytransaction
from PySide2.QtWidgets import QDialog, QApplication
from PySide2.QtCore import Signal, Slot
import sqlite3
from datetime import datetime


class newTransactionDialog(QDialog):
    
    dataready = Signal(object)
    depSelected = Signal(str)

    def __init__(self):
        super().__init__()
        self.data = {}
        self.ui = newtransaction.Ui_Dialog()
        self.ui.setupUi(self)
        self.accepted.connect(self.makedict)
        self.loadDepList()
        self.ui.department.currentIndexChanged.connect(self.loadEmpList)
    
    def loadDepList(self):
        with sqlite3.connect('test2.db') as conn:
            departments = conn.execute('select * from departments')
        self.departments = [dep[0] for dep in departments.fetchall()]
        self.ui.department.addItems(self.departments)

    @Slot()
    def loadEmpList(self):
        self.ui.employee.clear()
        department = self.ui.department.currentText()
        with sqlite3.connect('test2.db') as conn:
            employees = conn.execute('select empid, "empname" from employees where department = :dept',{'dept':department})
        self.employees = {emp[1]:emp[0] for emp in employees.fetchall()}
        self.ui.employee.addItems(list(self.employees.keys()))
        
    def makedict(self):
        date = datetime.strptime(self.ui.date.text(), '%d-%m-%y')
        date = datetime.strftime(date,'%Y-%m-%d')
        department = self.ui.department.currentText()
        try:
            empid = self.employees[self.ui.employee.currentItem().text()]
        except:
            pass
        
        credit = self.ui.credit.text()
        debit = self.ui.debit.text()
        self.data = {'date':date, 'department':department, 'empid':empid, 'credit':credit, 'debit':debit}
        self.dataready.emit(self.data)
        


class dispTransactionDialog(QDialog):
    
    dataready = Signal(object)
    depSelected = Signal(str)

    def __init__(self):
        super().__init__()
        self.data = {}
        self.ui = displaytransaction.Ui_Dialog()
        self.ui.setupUi(self)
        self.accepted.connect(self.makedict)
        self.loadDepList()
        self.ui.department.currentIndexChanged.connect(self.loadEmpList)
    
    def loadDepList(self):
        with sqlite3.connect('test2.db') as conn:
            departments = conn.execute('select * from departments')
        self.departments = [dep[0] for dep in departments.fetchall()]
        self.ui.department.addItems(self.departments)

    @Slot()
    def loadEmpList(self):
        self.ui.employee.clear()
        department = self.ui.department.currentText()
        with sqlite3.connect('test2.db') as conn:
            employees = conn.execute('select empid, "empname" from employees where department = :dept',{'dept':department})
        self.employees = {emp[1]:emp[0] for emp in employees.fetchall()}
        self.ui.employee.addItems(list(self.employees.keys()))
        
    def makedict(self):
        todate = datetime.strptime(self.ui.todate.text(), '%d-%m-%y')
        todate = datetime.strftime(todate,'%Y-%m-%d')
        fromdate = datetime.strptime(self.ui.fromdate.text(), '%d-%m-%y')
        fromdate = datetime.strftime(fromdate,'%Y-%m-%d')
        department = self.ui.department.currentText()
        try:
            empid = self.employees[self.ui.employee.currentItem().text()]
        except:
            pass
        
        credit = self.ui.credit.text()
        debit = self.ui.debit.text()
        self.data = {'todate':todate,'fromdate':fromdate, 'department':department, 'empid':empid, 'credit':credit, 'debit':debit}
        self.dataready.emit(self.data)


