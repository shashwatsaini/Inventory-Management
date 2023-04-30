import pandas as pd
import sys
import datetime
import re
from PyQt5.QtWidgets import QApplication, QScrollArea, QLabel, QGridLayout,QPushButton, QWidget, QGroupBox, QVBoxLayout, QLineEdit, QMenuBar, QAction, QMainWindow, QFileDialog, QSizePolicy, QComboBox, QSpinBox

GROUPBOX_HEIGHT= 60
LABEL_WIDTH= 1055

class bills(QWidget):
    def __init__(self, main_database_path, vendor_database_path):
        self.main_database_path= main_database_path
        self.vendor_database_path= vendor_database_path
        super().__init__()
        self.title= 'Create Bill'
        self.left= 0
        self.top= 0
        self.width=1200
        self.height=700

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.chosen_itemLayout= QGridLayout()
        self.chosen_itemLayout.setSpacing(10)
        self.chosen_item_groupbox= QGroupBox()
        self.itemLayout= QGridLayout()
        self.itemLayout.setSpacing(10)
        self.item_groupbox= QGroupBox()
        self.layout= QGridLayout()
        self.layout.setSpacing(10)

        self.items=[]
        self.spinBox=[]
        self.count=[]

        self.chosen_items=[]
        self.chosen_spinBox=[]
        
        self.search_button= QPushButton('Search')

        self.getdata()
        self.initialise_itemList()
        
        self.name_field= QLineEdit()
        self.name_field.setPlaceholderText('Enter Customer\'s Name')
        self.phone_field= QLineEdit()
        self.phone_field.setPlaceholderText('Enter Phone Number')
        self.search_option= QComboBox()
        self.search_option.addItem('Search by Name')
        self.search_option.addItem('Search by UPC')
        self.search_field= QLineEdit()
        self.search_field.setPlaceholderText('Search')
        self.search_button.clicked.connect(self.search)
        self.submit_button= QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit)

        self.chosen_item_groupbox.setLayout(self.chosen_itemLayout)
        self.chosen_itemScroll= QScrollArea()
        self.chosen_itemScroll.setWidget(self.chosen_item_groupbox)

        self.item_groupbox.setLayout(self.itemLayout)
        self.itemScroll= QScrollArea()
        self.itemScroll.setWidget(self.item_groupbox)

        self.layout.addWidget(self.name_field, 0,0,1,2)
        self.layout.addWidget(self.phone_field, 0,2,1,2)
        self.layout.addWidget(self.chosen_itemScroll, 1,0,3,-1)
        self.layout.addWidget(self.search_field,4,0,1,-1)
        self.layout.addWidget(self.search_button,5,0,1,2)
        self.layout.addWidget(self.search_option,5,2,1,2)
        self.layout.addWidget(self.itemScroll,6,0,3,-1)
        self.layout.addWidget(self.submit_button,9,3,1,1)

        self.setLayout(self.layout)
        self.show()

    def getdata(self):
        self.FILE= pd.read_csv(self.main_database_path)
        size= self.FILE.shape
        for i in range(size[0]):
            self.count.append(0)

    def initialise_itemList(self):
        size= self.FILE.shape
        self.items=[]
        self.spinBox=[]
        self.item_groupbox.setMinimumHeight(size[0]*GROUPBOX_HEIGHT)
        self.item_groupbox.setMaximumHeight(size[0]*GROUPBOX_HEIGHT)
        for i in range(size[0]):
            templabel= QLabel(self.FILE.iloc[i][0])
            templabel.setFixedWidth(LABEL_WIDTH)
            templabel.setWordWrap(True)
            self.items.append(templabel)
            tempspinbox= QSpinBox()
            tempspinbox.setValue(self.count[i])
            tempspinbox.valueChanged.connect(self.update_chosen_itemLayout)
            tempspinbox.setMaximumSize(80,40)
            self.spinBox.append(tempspinbox)
        for i in reversed(range(self.itemLayout.count())):
            self.itemLayout.itemAt(i).widget().setParent(None)
        for i in range(size[0]):
            self.itemLayout.addWidget(self.items[i], i, 0)
            self.itemLayout.addWidget(self.spinBox[i], i, 1)
        self.search_button.setText('Search')
        self.chosen_items= self.items        

    def search(self):
        if self.search_button.text()=='Search':
            size= self.FILE.shape
            key=''
            if self.search_option.currentIndex()==0:
                key= self.search_field.text()
                for i in reversed(range(self.itemLayout.count())):
                    self.itemLayout.itemAt(i).widget().setParent(None)
                count=0
                new_label_list=[]
                new_spinbox_list=[]
                for i in range(size[0]):
                    self.search_check= self.FILE.iloc[i][0].find(key)
                    templabel= QLabel(self.FILE.iloc[i][0])
                    new_label_list.append(templabel)
                    tempspinbox= QSpinBox()
                    tempspinbox.setValue(self.count[i])
                    new_spinbox_list.append(tempspinbox)
                    if self.search_check!=-1:
                        count+=1
                        new_label_list[-1].setFixedWidth(LABEL_WIDTH)
                        new_label_list[-1].setWordWrap(True)
                        new_spinbox_list[-1].setValue(self.count[i])
                        new_spinbox_list[-1].valueChanged.connect(self.update_chosen_itemLayout)
                        new_spinbox_list[-1].setMaximumSize(80,40)                    
                        self.itemLayout.addWidget(new_label_list[-1], count, 0)
                        self.itemLayout.addWidget(new_spinbox_list[-1], count, 1)
                self.item_groupbox.setMinimumHeight(count*GROUPBOX_HEIGHT)
                self.item_groupbox.setMaximumHeight(count*GROUPBOX_HEIGHT)
                self.search_button.setText('Reset')
                self.items= new_label_list
                self.spinBox= new_spinbox_list
            
            if self.search_option.currentIndex()==1:
                key= self.search_field.text()
                for i in reversed(range(self.itemLayout.count())):
                    self.itemLayout.itemAt(i).widget().setParent(None)
                count=0
                new_label_list=[]
                new_spinbox_list=[]
                for i in range(size[0]):
                    self.search_check= str(self.FILE.iloc[i][3]).find(key)
                    templabel= QLabel(str(self.FILE.iloc[i][0]))
                    new_label_list.append(templabel)
                    tempspinbox= QSpinBox()
                    tempspinbox.setValue(self.count[i])
                    new_spinbox_list.append(tempspinbox)
                    if self.search_check!=-1:
                        count+=1
                        new_label_list[-1].setFixedWidth(LABEL_WIDTH)
                        new_label_list[-1].setWordWrap(True)
                        new_spinbox_list[-1].valueChanged.connect(self.update_chosen_itemLayout)
                        new_spinbox_list[-1].setMaximumSize(80,40)                    
                        self.itemLayout.addWidget(new_label_list[-1], count, 0)
                        self.itemLayout.addWidget(new_spinbox_list[-1], count, 1)
                self.item_groupbox.setMinimumHeight(count*GROUPBOX_HEIGHT)
                self.item_groupbox.setMaximumHeight(count*GROUPBOX_HEIGHT)
                self.search_button.setText('Reset')
                self.items= new_label_list
                self.spinBox= new_spinbox_list
        else:
            self.initialise_itemList()

    #Adds in the items the customer has bought
    def update_chosen_itemLayout(self):
        size= self.FILE.shape
        count=0
        new_label_list=[]
        new_spinbox_list=[]
        for i in range(self.chosen_itemLayout.count()-1, -1, -1):
            self.chosen_itemLayout.itemAt(i).widget().setParent(None)
        for i in range(size[0]):
            self.count[i]= int(self.spinBox[i].value())
            templabel= QLabel(str(self.FILE.iloc[i][0]))
            new_label_list.append(templabel)
            tempspinbox= QSpinBox()
            tempspinbox.setValue(int(self.count[i]))
            new_spinbox_list.append(tempspinbox)
            if self.count[i]>0:
                new_label_list[-1].setFixedWidth(LABEL_WIDTH)
                new_label_list[-1].setWordWrap(True)
                new_spinbox_list[-1].valueChanged.connect(self.update_spinBox)
                new_spinbox_list[-1].setMaximumSize(80,40)                    
                self.chosen_itemLayout.addWidget(new_label_list[-1], count, 0)
                self.chosen_itemLayout.addWidget(new_spinbox_list[-1], count, 1)
                count+=1
        self.chosen_item_groupbox.setMinimumHeight((count)*GROUPBOX_HEIGHT)
        self.chosen_item_groupbox.setMaximumHeight((count)*GROUPBOX_HEIGHT)
        self.chosen_item_groupbox.setMinimumWidth(self.item_groupbox.width())
        self.chosen_items= new_label_list
        self.chosen_spinBox= new_spinbox_list

    #To make sure the values of both the sets of spinboxes are the same
    def update_spinBox(self):
        for i in range(len(self.chosen_spinBox)):
            if int(self.chosen_spinBox[i].value())>0:
                self.count[i]= int(self.chosen_spinBox[i].value())
        self.initialise_itemList()

    def submit(self):
        stream=''           #For mainlist.csv
        stream2=''          #For customers.csv
        size=self.FILE.shape
        current_date= datetime.datetime.now()
        current_date= current_date.strftime('%Y-%m-%d')
        dateFound=0
        for i in range(size[0]):
            if self.chosen_spinBox[i].value()>0:
                raw= self.FILE.at[i,'SALES']
                formatted= re.findall(r'\[(.*?)\]', raw)
                dates=[j.split('(')[0] for j in formatted]
                for j in range(len(dates)):
                    if dates[j]==current_date:
                        temp= re.findall(r'\((.*?)\)', formatted[j])[0]
                        templist=temp.split(',')
                        templist[1]=int(templist[1]) + int(self.chosen_spinBox[i].value())
                        formatted[j]= str(current_date) + '(' + str(templist[0]) + ',' + str(templist[1]) +')'
                        for k in formatted:
                            stream+= '[' + k + ']'
                        self.FILE.at[i,'SALES']= stream
                        self.FILE.at[i, 'Stock']= int(self.FILE.at[i, 'Stock']) - int(self.chosen_spinBox[i].value())
                        dateFound=1
                        break
                if dateFound==0:
                    self.FILE.at[i, 'SALES']= str(self.FILE.at[i, 'SALES']) + '[' + str(current_date) + '(' + str(self.FILE.at[i,'Name']) + ',' + str(self.chosen_spinBox[i].value()) + ')' +']'
                dateFound=0
                stream2+='(' + str(self.FILE.at[i,'Name']) + ',' + str(self.chosen_spinBox[i].value()) + ')'
                stream=''
        self.FILE.to_csv(self.main_database_path,index=False)
        try:
            customers=pd.read_csv('customers.csv')
        except:
            customers= pd.DataFrame(columns=['Name','Phone','ORDERS'])
            customers.to_csv('customers.csv', index=False)
        size= customers.shape
        customerFound=0
        for i in range(size[0]):
            if customers.at[i,'Name']==self.name_field.text() and customers.at[i, 'Phone']==self.phone_field.text():
                customers.at[i,'ORDERS']=str(customers.at[i,'ORDERS'])+ '[' + current_date + ',' + stream2 + ']'
                customerFound=1
                break
        if customerFound==0:
            new_customer= pd.DataFrame({'Name': self.name_field.text(), 'Phone': self.phone_field.text(), 'ORDERS':  ('[' + current_date + ',' + stream2 + ']')}, index=[0])
            customers= customers.append(new_customer, ignore_index=True)
            print(customers)
        customers.to_csv('customers.csv', index=False)
        self.close()
        #Add dates

if __name__=='__main__':
    App= QApplication(sys.argv)
    window= bills('mainlist.csv', 'vendors.csv')
    sys.exit(App.exec())