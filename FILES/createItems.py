from PyQt5.QtWidgets import QApplication, QGridLayout, QPushButton, QWidget, QLineEdit
import sys
from PyQt5 import QtGui, QtWidgets

class createItems(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Add Items"
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
        self.stock_field.setPlaceholderText('Enter Current Stock')
        self.stock_field.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.price_field = QLineEdit()
        self.price_field.setPlaceholderText('Enter the Price')
        self.price_field.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.upc_field = QLineEdit()
        self.upc_field.setPlaceholderText('Enter UPC')
        self.upc_field.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.submit_button = QPushButton('Submit')
        self.submit_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.submit_button.clicked.connect(self.submit)

        self.gridLayout.addWidget(self.name_field, 0, 0, 1, 3)
        self.gridLayout.addWidget(self.stock_field, 1, 0)
        self.gridLayout.addWidget(self.price_field, 1, 1)
        self.gridLayout.addWidget(self.upc_field, 1, 2)
        self.gridLayout.addWidget(self.submit_button, 2, 0)

        self.setLayout(self.gridLayout)
        self.show()

    def submit(self):
        text= self.name_field.text()
        text= text.strip()
        if text=='':
            self.name_field.setStyleSheet("color: rgb(255,0,0)")
        else:
            stream=''
            stock_field_text= self.stock_field.text()
            price_field_text= self.price_field.text()
            upc_field_text= self.upc_field.text()
            if stock_field_text=='':
                stock_field_text=0
            if price_field_text=='':
                price_field_text=0
            if upc_field_text=='':
                upc_field_text=0
            stream=self.name_field.text()+','+str(stock_field_text)+','+str(price_field_text)+','+str(upc_field_text)
            with open('addList.csv', 'w') as FILE:
                FILE.write(stream)
            self.close()

if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = createItems()
    sys.exit(App.exec())
