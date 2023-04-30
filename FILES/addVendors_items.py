#Need to fix search
from PyQt5.QtWidgets import QApplication, QScrollArea, QLabel, QGridLayout, QPushButton, QWidget, QGroupBox, QVBoxLayout, QLineEdit, QFrame, QHBoxLayout
import sys
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

GROUPBOX_HEIGHT= 50

class AddVendors_items(QWidget):
    def __init__(self, main_database_path, vendor_database_path):
        super().__init__()
        self.title= "Add Items"
        self.main_database_path= main_database_path
        self.vendor_database_path= vendor_database_path
        self.left= 0
        self.top= 0
        self.width= 1200
        self.height= 700

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.getdata()

        self.gridLayout= QGridLayout()
        self.gridLayout.setSpacing(10)
        self.groupBox= QGroupBox()

        self.drugs_list=[]
        self.button_list=[]
        self.select_list=[]

        self.search_button= QPushButton('Search')
        self.search_button.setMaximumHeight(70)
        self.search_button.clicked.connect(self.search)

        self.show_all()

        self.groupBox.setLayout(self.gridLayout)
        self.scroll= QScrollArea()
        self.scroll.setWidget(self.groupBox)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedHeight(650)

        self.layout= QVBoxLayout()
        selectLabel = QLabel('Select Items to Add')
        self.layout.addWidget(selectLabel)

        self.search_field= QLineEdit()
        self.search_field.setPlaceholderText('Search by Name')
        self.layout.addWidget(self.search_field)
        self.layout.addWidget(self.search_button)
        self.select_list_field= QLabel('Selected Items Appear Here')
        self.select_list_field.setFixedWidth(1170)
        self.select_list_field.setWordWrap(True)
        self.select_list_field.setFrameShape(QFrame.Box)
        self.layout.addWidget(self.select_list_field)

        self.layout.addWidget(self.scroll)

        self.submit_button = QPushButton('Submit')
        self.submit_button.setMaximumSize(80,40)
        self.layout.addWidget(self.submit_button)

        self.submit_button.clicked.connect(self.submit)

        self.setLayout(self.layout)

        self.show()

    def getdata(self):
        self.FILE= pd.read_csv(self.main_database_path)
    
    def show_all(self):
        self.drugs_list=[]
        self.button_list=[]

        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().setParent(None)

        size= self.FILE.shape
        for i in range(size[0]):
            templabel= QLabel(str(self.FILE.iloc[i][0]))
            templabel.setFixedWidth(1020)
            templabel.setWordWrap(True)
            self.drugs_list.append(templabel)
            tempbutton= QPushButton('Include')
            tempbutton.setMaximumSize(80,40)
            tempbutton.clicked.connect(self.on_button_clicked)
            self.button_list.append(tempbutton)
            self.gridLayout.addWidget(self.drugs_list[i], i, 0)
            self.gridLayout.addWidget(self.button_list[i], i, 1)
        self.search_button.setText('Search')
        self.groupBox.setMaximumHeight(int(GROUPBOX_HEIGHT*size[0]))

    def search(self):
        check= self.search_button.text() #To check current state of the button
        if check=='Search':
            key = self.search_field.text()
            new_drugs_list = []
            new_buttonlist = []
            for i in reversed(range(self.gridLayout.count())):
                self.gridLayout.itemAt(i).widget().setParent(None)
            count = 0
            size= self.FILE.shape
            for i in range(size[0]):
                current_search = str(self.FILE.iloc[i])
                search_check= current_search.find(key)
                if search_check != -1:
                    count += 1
                    templabel = QLabel(str(self.FILE.iloc[i][0]))
                    templabel.setFixedWidth(1020)
                    templabel.setWordWrap(True)
                    new_drugs_list.append(templabel)
                    tempbutton = QPushButton('Include')
                    tempbutton.setMaximumSize(80, 40)
                    tempbutton.clicked.connect(self.on_button_clicked)
                    new_buttonlist.append(tempbutton)
                    self.gridLayout.addWidget(new_drugs_list[-1], count, 0)
                    self.gridLayout.addWidget(new_buttonlist[-1], count, 1)
            self.groupBox.setMaximumHeight(count*GROUPBOX_HEIGHT)
            self.search_button.setText('Reset')
            self.drugs_list= new_drugs_list
            self.button_list= new_buttonlist
        else:
            self.show_all()

    def on_button_clicked(self):
        button= self.sender()
        index= self.button_list.index(button)
        if button.text()=='Include':
            self.select_list.append(self.FILE.iloc[index][0])
            button.setText('Added')
        else:
            self.select_list.remove(self.FILE.iloc[index][0])
            button.setText('Include')
        stream=''
        if len(self.select_list)==0:
            stream='Selected Items Appear Here'
        else:
            for i in range(len(self.select_list)): 
                temp= str(self.select_list[i])
                stream=stream+temp+', '
        self.select_list_field.setText(stream)
    
    def submit(self):
        stream=''
        for i in range(len(self.select_list)):
            temp= str(self.select_list[i])
            stream=stream+temp+', '
        with open('vendor_select_list.csv','w') as FILE:
            FILE.write(stream)
            print('Saved to vendor_select_list: '+ stream)
        self.close()

if __name__=='__main__':
    App= QApplication(sys.argv)
    window= AddVendors_items()
    sys.exit(App.exec())