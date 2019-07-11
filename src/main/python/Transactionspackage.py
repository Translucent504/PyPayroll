from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Qt
from PySide2.QtSql import (QSqlQuery, QSqlRelation, QSqlRelationalDelegate,
        QSqlRelationalTableModel, QSqlTableModel)
import sys
import sqlite3
import myobjects
from dataclasses import dataclass
import datetime
import pprint

# This is going to contain the Custom Model / Proxymodel / Tableview / widgetmapping/ sqlrelational bullshit and everything 
# relevant to transactions..

# model.setTable("transactions")
# model.setRelation(2, QSqlRelation('employees', 'empid', 'name')) the 2 corresponds to the field in transaction table
# name is what u retrieve from employees table
# Balance calculation query:


LUL = """SELECT date,"emp-name"
       credit,
       (SELECT sum(debit - credit)
        FROM transactionsnew AS T2
        WHERE T2.date <= transactionsnew.date and T2.empid = 23
       ) AS cumulative_sum
FROM transactionsnew inner join employees on transactionsnew.empid = employees.empid where transactionsnew.empid = 23
ORDER BY date;"""



@dataclass(order=True)
class transactionRecord:
    id: int
    name: str
    date: datetime.datetime
    amount: int
    description: str = ''



class newTransactionModel(QtCore.QAbstractTableModel):
    def __init__(self, employeeid, daterange=[]):
        super().__init__()
        self.employee = myobjects.Employee(employeeid)
        #self.department = myobjects.Department(department)
        #self.startdate = startdate
        #self.enddate = enddate
        #self.employees = self.department.employees
        #self.empids = [employee.id for employee in self.employees]
        #self.setTransactions()

    
    def getAllTransactions(self):
        with sqlite3.connect('test2.db') as conn:
            query = f'select * from transactionsnew where empid = {self.employee.id}'
            result = conn.execute(query).fetchall()
            print(result)
    @QtCore.Slot(object)
    def setDateRange(self, daterange):
        #print(enddate.toPython())
        self.daterange = daterange #??????
        self.setTransactions()
        
    def deletetransaction(self, index):
        transid = self.displaydata[index.row()]['transid']
        with sqlite3.connect('test2.db') as conn:
            conn.execute(f'delete from transactions where "transaction-id" = {transid}')
        self.setTransactions()    

    def setTransactions(self):
        
        with sqlite3.connect('test2.db') as conn:
            #{'empids':self.empids, 'startdate': f"{self.startyear}-{self.startmonth:02}-{self.startday:02}" ,'enddate': f"{self.endyear}-{self.endmonth:02}-{self.endday:02}"}
            query = f"SELECT * FROM transactions WHERE empid in ({','.join(['?']*len(self.empids))}) and date between '{self.startdate}' and '{self.enddate} order by date desc'"
            self.transactiondata = conn.execute(query, self.empids).fetchall()
        
            #transactiondata = conn.execute('select * from transactions where empid in (:empids) and date between :startdate and :enddate',{'startdate':self.startdate,'enddate':self.enddate,'empids':self.empids})
        
        self.displaydata = []
        for x in self.transactiondata:
            tmp = {}
            tmp['transid'] = x[0]
            tmp['empname'] = myobjects.Employee(x[1]).name
            tmp['date'] = x[2]
            tmp['amount'] = x[3]
            self.displaydata.append(tmp)

        self.headerDataChanged.emit(QtCore.Qt.Horizontal,0,self.columnCount()-1)

    def rowCount(self,parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return len(self.transactiondata)

    def columnCount(self,parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return 6

    def data(self, index, role):
        row, col = index.row(), index.column()
        if role == QtCore.Qt.DisplayRole:
            if col == 0:
                return self.displaydata[row]['empname']
            elif col == 1:
                return self.displaydata[row]['amount']
            elif col ==2:
                return self.displaydata[row]['date']

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            if section == 0:
                return "Date"
            if section == 1:
                return "Name"
            if section == 2:
                return "Type"
            if section == 3:
                return "Amount"
            if section == 4:
                return "Balance"
            if section == 5:
                return "Description"

    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            row, col = index.row(), index.column()
            transid = self.transactiondata[row][0]
            if col == 1:
                query = f'update transactions set amount = {value} where "transaction-id" = {transid}'
                with sqlite3.connect('test2.db') as conn:
                    conn.execute(query)
            elif col == 2:
                query = f'update transactions set date = {value} where "transaction-id" = {transid}'
                with sqlite3.connect('test2.db') as conn:
                    conn.execute(query)
            self.setTransactions()
            self.dataChanged.emit(index,index)
            return True
        return False

    def flags(self, index):
        if not index.column() == 0:
            return QtCore.Qt.ItemIsEditable | super().flags(index)
        else:
            return super().flags(index)


def getAllTransactions():
        with sqlite3.connect('test2.db') as conn:
            query = f'select * from transactionsnew where empid = {23}'
            result = conn.execute(LUL).fetchall()
            pprint.pprint(result)

getAllTransactions()
"""
app = QtWidgets.QApplication()
view = QtWidgets.QTableView()
view.show()
exitcode = app.exec_()
sys.exit(exitcode) 
"""