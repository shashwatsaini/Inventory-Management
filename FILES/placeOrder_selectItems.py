from PyQt5.QtWidgets import QApplication, QScrollArea, QLabel, QGridLayout, QPushButton, QWidget, QGroupBox, QLineEdit, QHBoxLayout, QFrame, QSpinBox
import sys
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
import datetime
import re

GROUPBOX_HEIGHT= 60
LABEL_WIDTH= 1080
class placeOrder_selectItems(QWidget):
    def __init__(self, vendor, vendor_name, main_database_path, vendors_database_path):
        super().__init__()
        self.actionCheck=0
        self.vendor=vendor
        self.vendor_name= vendor_name
        self.main_database_path= main_database_path
        self.vendors_database_path= vendors_database_path

        self.title= 'Place Order'
        
        self.left=0
        self.top=0
        self.width= 1200
        self.height= 700

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.gridLayout= QGridLayout()
        self.groupBox= QGroupBox()
        self.scroll= QScrollArea()
        self.layout= QGridLayout()
        self.layout.setVerticalSpacing(10)

        self.remark_field= QLineEdit()
        self.remark_field.setPlaceholderText('Enter Remarks')
        self.remark_field.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.select_field= QLabel('Selected Items Appear Here')
        self.select_field.setWordWrap(True)
        self.select_field.setFrameShape(QFrame.Box)
        self.select_field.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.select_field.setMaximumHeight(30)

        self.search_field= QLineEdit()
        self.search_field.setPlaceholderText('Search')
        self.search_button= QPushButton('Search')
        self.search_button.clicked.connect(self.search)
        self.submit_button= QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit)

        self.gridLayout= QGridLayout()
        self.drugs_list=[]
        self.label_list=[]
        self.spinbox_list=[]
        self.count=[]

        self.getData()
        self.initialise_lists()

        self.groupBox.setLayout(self.gridLayout)
        self.scroll.setWidget(self.groupBox)
        self.layout.addWidget(self.remark_field,0,0,1,-1)
        self.layout.addWidget(self.select_field,1,0,1,-1)
        self.layout.addWidget(self.search_field,2,0,1,2)
        self.layout.addWidget(self.search_button,2,2)
        self.layout.addWidget(self.scroll,3,0,1,-1)
        self.layout.addWidget(self.submit_button,4,0)

        self.setLayout(self.layout)
        self.show()

    def getData(self):
        self.FILE= pd.read_csv(self.vendors_database_path)
        tempstr= self.FILE.loc[self.vendor]['Items']
        self.drugs_list= tempstr.split(' ')
        while '' in self.drugs_list:
            self.drugs_list.remove('')
        for i in range(len(self.drugs_list)):
            self.count.append(0)
    
    def initialise_lists(self):
        self.label_list=[]
        self.spinbox_list=[]
        size=len(self.drugs_list)
        self.groupBox.setMinimumHeight(size*GROUPBOX_HEIGHT)
        self.groupBox.setMaximumHeight(size*GROUPBOX_HEIGHT)
        for i in range(size):
            if self.drugs_list!='':
                templabel= QLabel(self.drugs_list[i])
                templabel.setFixedWidth(LABEL_WIDTH)
                templabel.setWordWrap(True)
                self.label_list.append(templabel)
                tempspinbox= QSpinBox()
                tempspinbox.setValue(self.count[i])
                tempspinbox.valueChanged.connect(self.update_select_field)
                tempspinbox.setMaximumSize(80,40)
                self.spinbox_list.append(tempspinbox)
        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().setParent(None)
        for i in range(size):
            self.gridLayout.addWidget(self.label_list[i], i, 0)
            self.gridLayout.addWidget(self.spinbox_list[i], i, 1)

        self.search_button.setText('Search')

    def search(self):
        check= self.search_button.text()
        if check=='Search':
            key= self.search_field.text()
            for i in reversed(range(self.gridLayout.count())):
                self.gridLayout.itemAt(i).widget().setParent(None)
            count=0
            new_label_list=[]
            new_spinbox_list=[]
            for i in range(len(self.drugs_list)):
                self.search_check= self.drugs_list[i].find(key)
                templabel= QLabel(self.drugs_list[i])
                new_label_list.append(templabel)
                tempspinbox= QSpinBox()
                new_spinbox_list.append(tempspinbox)
                if self.search_check!=-1:
                    count+=1
                    new_label_list[-1].setFixedWidth(LABEL_WIDTH)
                    new_label_list[-1].setWordWrap(True)
                    new_spinbox_list[-1].setValue(self.count[i])
                    new_spinbox_list[-1].valueChanged.connect(self.update_select_field)
                    new_spinbox_list[-1].setMaximumSize(80,40)                    
                    self.gridLayout.addWidget(new_label_list[-1], count, 0)
                    self.gridLayout.addWidget(new_spinbox_list[-1], count, 1)
            self.groupBox.setMinimumHeight(count*GROUPBOX_HEIGHT)
            self.groupBox.setMaximumHeight(count*GROUPBOX_HEIGHT)
            self.search_button.setText('Reset')
            self.label_list= new_label_list
            self.spinbox_list= new_spinbox_list
        else:
            self.initialise_lists()

    def update_select_field(self):
        select_field=''
        for i in range(len(self.drugs_list)):
            if self.spinbox_list[i].value()>0:
                self.count[i]= self.spinbox_list[i].value()
                select_field+=self.drugs_list[i]+','
        self.select_field.setText(select_field)

    def submit(self):
        FILE= pd.read_csv(self.main_database_path)
        size= FILE.shape
        order_save=''
        new_val=''
        current_date= datetime.datetime.now()
        current_date= current_date.strftime('%Y-%m-%d')
        dateFound=0
        for i in range(size[0]):
            key= FILE.iloc[i][0]
            raw= FILE.at[i,'HISTORY']
            formatted= re.findall(r'\((.*?)\)', raw)
            dates = [date.split(',')[0].strip() for date in formatted]
            for a in range(len(dates)):
                dates[a]= dates[a].replace('\'', '')
                dates[a]= dates[a].replace('\'', '')
                count= [a.split(',')[1].strip() for a in formatted]
            for j in range(len(self.drugs_list)):
                if key==self.drugs_list[j] and self.spinbox_list[j].value()>0:        
                    for k in range(len(dates)):
                        if dates[k]==current_date:
                            #new_val= str((current_date.strftime('%Y-%m-%d'), int(FILE.iloc[i][1])+int(self.spinbox_list[j].value()), self.vendor_name))
                            new_count= int(count[k])+ int(self.spinbox_list[j].value())
                            formatted[k]= str(dates[k]) + ',' + str(new_count) + ',' + str(self.vendor_name)
                            for b in formatted:
                                new_val+= '(' + str(b) + ')'
                            dateFound=1
                            break
                    if dateFound==1:
                        FILE.at[i,'HISTORY']= new_val
                        print(i)
                        new_val=''
                        dateFound=0
                        print('control2')
                    elif dateFound==0:
                        old_val= FILE.at[i, 'HISTORY']
                        new_val= str((current_date, int(FILE.iloc[i][1])+int(self.spinbox_list[j].value()), self.vendor_name))
                        new_val= old_val+new_val
                        FILE.at[i, 'HISTORY']= new_val
                        new_val=''
                        old_val=''
                    stock=float(FILE.at[i, 'Stock'])
                    stock+=self.spinbox_list[j].value()
                    FILE.at[i,'Stock']= stock

                    #For vendors.csv:
                    order_save+= str((key, current_date, stock))
                    break
        FILE.to_csv(self.main_database_path, index=False)
        vendors= pd.read_csv(self.vendors_database_path)
        final_order_save= str(vendors.at[self.vendor,'ORDERS'])
        final_order_save+=order_save
        vendors.at[self.vendor,'ORDERS']= final_order_save
        remarks_save= str(vendors.at[self.vendor, 'REMARKS'])
        remarks_save+=str((current_date, self.remark_field.text()))
        vendors.at[self.vendor, 'REMARKS']= remarks_save
        vendors.to_csv(self.vendors_database_path, index=False)
        self.close()


if __name__=='__main__':
    App= QApplication(sys.argv)
    window= placeOrder_selectItems(0, 'vendor1', 'mainlist.csv','vendors.csv')
    sys.exit(App.exec())
