from PyQt5.QtWidgets import QApplication, QGridLayout, QPushButton, QWidget, QLineEdit
import sys
from PyQt5 import QtGui, QtWidgets
import pandas as pd


class manageItem(QWidget):
    def __init__(self, item, main_database_path, vendor_database_path):
        super().__init__()
        self.item= item
        self.main_database_path= main_database_path
        self.vendor_database_path= vendor_database_path
        self.index=-1
        
        self.title = "Manage Item"
        self.left = 0
        self.top = 0
        self.width = 700
        self.height = 150

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(20)

        self.name_field = QLineEdit()
        self.name_field.setPlaceholderText('Enter Name')
        self.name_field.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.stock_field = QLineEdit()
        self.stock_field.setInputMask('D9999')
        self.stock_field.setPlaceholderText('Enter Current Stock')
        self.stock_field.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.price_field = QLineEdit()
        self.price_field.setInputMask('D9999')
        self.price_field.setPlaceholderText('Enter the Price')
        self.price_field.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.upc_field = QLineEdit()
        self.upc_field.setPlaceholderText('Enter UPC')
        self.upc_field.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.submit_button = QPushButton('Submit')
        self.submit_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.submit_button.clicked.connect(self.submit)

        self.getdata()

        self.gridLayout.addWidget(self.name_field, 0, 0, 1, 3)
        self.gridLayout.addWidget(self.stock_field, 1, 0)
        self.gridLayout.addWidget(self.price_field, 1, 1)
        self.gridLayout.addWidget(self.upc_field, 1, 2)
        self.gridLayout.addWidget(self.submit_button, 2, 0)

        self.setLayout(self.gridLayout)
        self.show()

    def getdata(self):
        self.FILE= pd.read_csv(self.main_database_path)
        for i in range((self.FILE.shape)[0]):
            if self.FILE.iloc[i][0]==self.item:
                self.index=i
                break

        self.name_field.setPlaceholderText('Current Name: '+str(self.FILE.iloc[i][0]))
        self.stock_field.setPlaceholderText('Current Stock: '+str(self.FILE.at[i,'Stock']))
        self.price_field.setPlaceholderText('Current Price: '+str(self.FILE.at[i, 'Price']))
        self.upc_field.setPlaceholderText('Current UPC: '+str(self.FILE.at[i, 'UPC']))

    def submit(self):
        name= self.name_field.text()
        name= name.strip()
        if name!='':
            self.FILE.at[self.index, 'Name']= name
        price= self.price_field.text()
        price= price.strip()
        if price!='':
            self.FILE.at[self.index, 'Price']= int(price)
        stock= self.stock_field.text()
        stock= stock.strip()
        if stock!='':
            self.FILE.at[self.index, 'Stock']= int(stock)
        upc= self.upc_field.text()
        upc= upc.strip()
        if upc!='':
            self.FILE.at[self.index, 'UPC']= upc
        self.FILE.to_csv(self.main_database_path, index=False)
        self.close()

if __name__=='__main__':
    App = QApplication(sys.argv)
    window = manageItem('KALIBICHROMICUM', 'mainlist.csv', 'vendors.csv')
    sys.exit(App.exec())
