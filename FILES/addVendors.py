from PyQt5.QtWidgets import QApplication, QScrollArea, QLabel, QGridLayout, QPushButton, QWidget, QGroupBox, QVBoxLayout, QLineEdit, QFrame, QHBoxLayout
import sys
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from FILES.addVendors_items import AddVendors_items
import datetime

class addVendors(QWidget):
    def __init__(self, main_database_path, vendor_database_path):
        super().__init__()
        self.title='Add Vendors'
        self.main_database_path= main_database_path
        self.vendor_database_path= vendor_database_path

        self.left=0
        self.top=0
        self.width=700
        self.height=150

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.actionCheck=0

        self.gridLayout= QGridLayout()
        self.gridLayout.setSpacing(20)
        self.name_field= QLineEdit()
        self.name_field.setPlaceholderText('Enter Name')
        self.name_field.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            
        self.email_field= QLineEdit()
        self.email_field.setPlaceholderText('Email Address')
        self.email_field.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.phone_field= QLineEdit()
        self.phone_field.setPlaceholderText('Phone Number')
        self.phone_field.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.text1= QLabel('Enter materials sourced here:')
        self.add_button= QPushButton('Add')
        self.add_button.clicked.connect(self.add)
        self.select_field= QLabel('Selected Items Appear Here')
        self.select_field.setWordWrap(True)
        self.select_field.setFrameShape(QFrame.Box)
        self.refresh_button= QPushButton('Refresh')
        self.refresh_button.clicked.connect(self.refresh)
        self.submit_button= QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit)

        self.gridLayout.addWidget(self.name_field,0,0,1,2)
        self.gridLayout.addWidget(self.email_field, 1,0)
        self.gridLayout.addWidget(self.phone_field,1,1)
        self.gridLayout.addWidget(self.text1,2,0)
        self.gridLayout.addWidget(self.add_button,2,1)
        self.gridLayout.addWidget(self.select_field, 3,0,1,2)
        self.gridLayout.addWidget(self.refresh_button,4,0)
        self.gridLayout.addWidget(self.submit_button,4,1)

        self.setLayout(self.gridLayout)
        self.show()
        
    def add(self):
        self.actionCheck=1
        self.temp_window= AddVendors_items(self.main_database_path, self.vendor_database_path)
        self.temp_window.show()

    def refresh(self):
        if self.actionCheck==1:
            with open('vendor_select_list.csv','r') as FILE:
                stream= FILE.readline()
                self.select_field.setText(stream)
            self.actionCheck=0
            with open('vendor_select_list.csv', 'w') as FILE:
                stream=''
                FILE.write(stream)

    def submit(self):
        FILE= pd.read_csv(self.vendor_database_path)
        current_time= datetime.datetime.now()
        date= current_time.date()
        string_items= self.select_field.text().replace(',', '')
        new_row= pd.DataFrame({'Name': self.name_field.text(), 'Email': self.email_field.text(), 'Phone': self.phone_field.text(), 'Items': string_items, 'Date_Added': str(date), 'ORDERS': 0, 'REMARKS':0}, index=[0])
        FILE= FILE.append(new_row, ignore_index= True)
        FILE.to_csv(self.vendor_database_path, index= False)
        self.close()

if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = addVendors()
    sys.exit(App.exec())