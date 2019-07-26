from PySide2.QtWidgets import QLineEdit, QLabel, QComboBox, QGridLayout, QPushButton, QApplication, QWidget
import sqlite3
from datetime import datetime


class updateEmployee(QWidget):
    """
    Dialog box to add a new employee.
    Fields:
    Name, Department, Designation, Salary, Salary Structure, Overtime rate, Working status
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Employee Info")
        self.mainlayout = QGridLayout()
        self.name = QLineEdit(self)
        self.name.setObjectName("name")
        self.label1 = QLabel("Name:")
        self.label2 = QLabel("Department")
        self.depart = QComboBox(self)
        self.depart.setObjectName("depart")
        with sqlite3.connect('test2.db') as conn:
            self.departlist = conn.execute('select * from departments').fetchall()
        self.departlist = [x[0] for x in self.departlist]
        self.depart.addItems(self.departlist)
        self.mainlayout.addWidget(self.name, 0, 1)
        self.mainlayout.addWidget(self.depart, 1, 1)
        self.mainlayout.addWidget(self.label1, 0, 0)
        self.mainlayout.addWidget(self.label2, 1, 0)
        self.label3 = QLabel("Designation")
        self.designation = QComboBox(self)
        self.designation.setObjectName("designation")
        self.designation.addItems(["Helper" ,"Operator"])
        self.mainlayout.addWidget(self.label3, 2, 0)
        self.mainlayout.addWidget(self.designation,2,1)
        self.label4 = QLabel("Salary")
        self.salary = QLineEdit(self)
        self.salary.setObjectName("salary")
        self.label5 = QLabel("Salary Structure")
        self.salarystruct = QComboBox(self)
        self.salarystruct.setObjectName("salarystruct")
        self.salarystruct.addItems(["Monthly","Daily"])
        self.label6 = QLabel("Overtime rate")
        self.overtime = QLineEdit(self)
        self.overtime.setObjectName("overtime")
        self.label7 = QLabel("Working Status")
        self.working = QComboBox(self)
        self.working.setObjectName("working")
        self.working.addItems(["Working","Terminated"])
        self.date = QLineEdit(self)
        self.date.setClearButtonEnabled(True)
        self.date.setInputMask("00-00-00")
        tmpdate = datetime.strftime(datetime.now(),'%d-%m-%y')
        self.date.setText(tmpdate)
        self.rejectbtn = QPushButton("Close")
        self.label8 = QLabel("Termination Date:")
        self.mainlayout.addWidget(self.label4, 3, 0)
        self.mainlayout.addWidget(self.salary, 3, 1)
        self.mainlayout.addWidget(self.label5, 4, 0)
        self.mainlayout.addWidget(self.salarystruct, 4, 1)
        self.mainlayout.addWidget(self.label6, 5, 0)
        self.mainlayout.addWidget(self.overtime, 5, 1)
        self.mainlayout.addWidget(self.label7, 6, 0)
        self.mainlayout.addWidget(self.working, 6, 1)
        self.mainlayout.addWidget(self.label8, 7, 0)
        self.mainlayout.addWidget(self.date, 7, 1)
        self.mainlayout.addWidget(self.rejectbtn, 8, 1)
        self.working.currentIndexChanged.connect(self.enableTerminationDate)
        self.rejectbtn.clicked.connect(self.close)
        self.setLayout(self.mainlayout)
        self.setFocusProxy(self.name)


    def enableTerminationDate(self):
        if self.working.currentText() == "Terminated":
            self.date.setEnabled(True)
        else:
            self.date.setEnabled(False)
        
