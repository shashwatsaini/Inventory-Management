from PyQt5.QtWidgets import QApplication, QScrollArea, QLabel, QGridLayout, QPushButton, QWidget, QGroupBox, QLineEdit, QHBoxLayout
import sys
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from FILES.addVendors import addVendors

GROUPBOX_HEIGHT= 60

class Vendors(QWidget):
    def __init__(self, main_database_path, vendors_database_path):
        super().__init__()

        self.actionCheck=0
        self.main_database_path= main_database_path
        self.vendors_database_path= vendors_database_path

        self.title= 'Manage Vendors'
        
        self.left=0
        self.top=0
        self.width= 1200
        self.height= 700

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.gridLayout= QGridLayout()
        self.groupBox= QGroupBox()
        self.layout= QGridLayout()
        self.layout.setVerticalSpacing(10)

        self.vendors_list=[]
        self.buttons_list=[]
        self.email_list=[]
        self.phone_list=[]

        self.search_button= QPushButton('Search')

        self.getdata()
        self.initialise_lists()

        self.search_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.search_button.setMaximumHeight(70)
        self.search_button.clicked.connect(self.search)
        self.search_field= QLineEdit()
        self.search_field.setPlaceholderText('Search by Name')
        self.search_field.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.add_button= QPushButton('Add Vendors')
        self.add_button.clicked.connect(self.add)
        self.add_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.refresh_button= QPushButton('Refresh')
        self.refresh_button.clicked.connect(self.refresh)
        self.refresh_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        refresh_add_layout = QHBoxLayout()
        refresh_add_layout.addStretch(1)
        refresh_add_layout.addWidget(self.add_button)
        refresh_add_layout.addWidget(self.refresh_button)
        refresh_add_layout.setAlignment(Qt.AlignLeft)

        self.groupBox.setLayout(self.gridLayout)
        self.scroll= QScrollArea()
        self.scroll.setWidget(self.groupBox)
        self.scroll.setWidgetResizable(True)
        self.scroll.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.scroll.setFixedHeight(600)

        self.layout.addWidget(self.search_field,0,0,1,-1)
        self.layout.addWidget(self.search_button,1,0,1,-1)
        self.layout.addWidget(self.scroll,2,0,2,4)
        self.layout.addLayout(refresh_add_layout, 4, 3,1,-1)

        self.setLayout(self.layout)
        self.show()

    def getdata(self):    
        self.FILE= pd.read_csv(self.vendors_database_path)

    def initialise_lists(self):
        self.vendors_list=[]
        self.buttons_list=[]
        self.email_list=[]
        self.phone_list=[]
        size= self.FILE.shape
        for i in range(size[0]):
            templabel = QLabel(str(self.FILE.iloc[i][0]))#For name
            templabel.setWordWrap(True)
            self.vendors_list.append(templabel)

            templabel2= QLabel(str(self.FILE.iloc[i][1]))#For email
            templabel2.setWordWrap(True)
            self.email_list.append(templabel2)

            templabel3= QLabel(str(self.FILE.iloc[i][2]))#For phone
            templabel3.setWordWrap(True)
            self.phone_list.append(templabel3)

            tempbutton= QPushButton('Manage')
            tempbutton.setMaximumSize(80,40)
            tempbutton.clicked.connect(self.on_button_clicked)
            self.buttons_list.append(tempbutton)
        self.groupBox.setMaximumHeight(GROUPBOX_HEIGHT*size[0])
        self.search_button.setText('Search')

        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().setParent(None)

        for i in range(size[0]):
            self.gridLayout.addWidget(self.vendors_list[i], i, 0)
            self.gridLayout.addWidget(self.email_list[i], i, 1)
            self.gridLayout.addWidget(self.phone_list[i], i, 2)
            self.gridLayout.addWidget(self.buttons_list[i], i, 3)
        
        self.groupBox.setMaximumHeight(int(GROUPBOX_HEIGHT*size[0]))
        self.FILE.to_csv('vendors.csv', index=False)

    def on_button_clicked(self):
        pass

    def add(self):
        self.actionCheck=1
        self.tempwindow= addVendors(self.main_database_path, self.vendors_database_path)
        self.tempwindow.show()

    def refresh(self):
        if self.actionCheck==1:
            self.getdata()
            self.initialise_lists()
            self.actionCheck=0

    def search(self):
        check= self.search_button.text()
        if check=='Search':
            key= self.search_field.text()
            new_vendors_list=[]
            new_email_list=[]
            new_phone_list=[]
            new_buttons_list=[]
            for i in reversed(range(self.gridLayout.count())):
                self.gridLayout.itemAt(i).widget().setParent(None)
            count=0
            size= self.FILE.shape
            current_index=0         #To remember the index for addding the elements to the scroll area
            for i in range(size[0]):
                search_check= self.FILE.iloc[i][0].find(key)
                if search_check !=-1 or key=='' or key==' ':
                    count+=1
                    templabel = QLabel(str(self.FILE.iloc[i][0]))#For name
                    templabel.setWordWrap(True)
                    new_vendors_list.append(templabel)

                    templabel2= QLabel(str(self.FILE.iloc[i][1]))#For email
                    templabel2.setWordWrap(True)
                    new_email_list.append(templabel2)

                    templabel3= QLabel(str(self.FILE.iloc[i][2]))#For phone
                    templabel3.setWordWrap(True)
                    new_phone_list.append(templabel3)

                    tempbutton= QPushButton('Manage')
                    tempbutton.setMaximumSize(80,40)
                    tempbutton.clicked.connect(self.on_button_clicked)
                    new_buttons_list.append(tempbutton)

                    self.gridLayout.addWidget(new_vendors_list[-1], current_index, 0)
                    self.gridLayout.addWidget(new_email_list[-1], current_index, 1)
                    self.gridLayout.addWidget(new_phone_list[-1], current_index, 2)
                    self.gridLayout.addWidget(new_buttons_list[-1], current_index, 3)

                    current_index+=1

            self.groupBox.setMaximumHeight(current_index*GROUPBOX_HEIGHT)
                    
            self.search_button.setText('Reset')
            self.vendors_list= new_vendors_list
            self.email_list= new_email_list
            self.phone_list= new_phone_list
            self.buttons_list= new_buttons_list  
        else:
            self.search_button.setText('Search')
            self.initialise_lists()    
                    

if __name__=='__main__':
    App= QApplication(sys.argv)
    window= Vendors()
    sys.exit(App.exec())
