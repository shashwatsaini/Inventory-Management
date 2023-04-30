from PyQt5.QtWidgets import QApplication, QScrollArea, QLabel, QGridLayout,QPushButton, QWidget, QGroupBox, QVBoxLayout, QLineEdit, QFrame
import sys
import pandas as pd

pd.options.display.max_rows=10000
GROUPBOX_HEIGHT= 60

class addItems(QWidget):
    def __init__(self, raw_database_path):
        super().__init__()
        self.raw_database_path= raw_database_path
        self.data=[]
        self.select_list=[]
        self.getdata(500)

        self.title= "Add Items from Database"
        self.left= 0
        self.top= 0
        self.width= 1200
        self.height= 700

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.gridLayout= QGridLayout()
        self.gridLayout.setSpacing(10)
        self.groupBox= QGroupBox()

        global drugs_list
        drugs_list=[]
        global buttonlist
        buttonlist=[]

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
    
    def show_all(self):
        global drugs_list, buttonlist
        drugs_list=[]
        buttonlist=[]
        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().setParent(None)
        for i in range(len(self.data)):
            templabel= QLabel(str(self.data[i]))
            templabel.setFixedWidth(1020)
            templabel.setWordWrap(True)
            drugs_list.append(templabel)
            tempbutton= QPushButton('Include')
            tempbutton.setMaximumSize(80,40)
            tempbutton.clicked.connect(self.on_button_clicked)
            buttonlist.append(tempbutton)
            self.gridLayout.addWidget(drugs_list[i], i, 0)
            self.gridLayout.addWidget(buttonlist[i], i, 1)
        self.groupBox.setMaximumHeight(GROUPBOX_HEIGHT*len(self.data))
        self.search_button.setText('Search')

    def on_button_clicked(self):
        global buttonlist
        button = self.sender()
        index = buttonlist.index(button)
        if button.text()=='Include':
            self.select_list.append(self.data[index])
            button.setText('Added')
        else:
            self.select_list.remove(self.data[index])
            button.setText('Include')
        stream=''
        if len(self.select_list)==0:
            stream='Selected Items Appear Here'
        else:
            for i in range(len(self.select_list)): 
                temp= str(self.select_list[i])
                temp_list= temp.split('-')
                temp= temp_list[1]
                stream=stream+temp+', '
        self.select_list_field.setText(stream)

    def submit(self): #Append this to a dataframe, turn addItems_list into a dataframe
        stream=''
        for i in range(len(self.select_list)):
            temp= str(self.select_list[i])
            temp_list= temp.split('-')
            temp= temp_list[1]
            stream=stream+temp+', '
        with open('addItems.csv','w') as FILE:
            FILE.write(stream)
            print('Saved to addItems: '+ stream)
        self.close()
        
    
    def search(self):
        check= self.search_button.text() #To check current state of the button
        if check=='Search':
            key = self.search_field.text()
            new_drugs_list = []
            new_buttonlist = []
            for i in reversed(range(self.gridLayout.count())):
                self.gridLayout.itemAt(i).widget().setParent(None)
            count = 0
            for i in range(len(self.data)):
                search_check = self.data[i].find(key)
                if search_check != -1:
                    count += 1
                    templabel = QLabel(str(self.data[i]))
                    templabel.setFixedWidth(1020)
                    templabel.setWordWrap(True)
                    new_drugs_list.append(templabel)
                    tempbutton = QPushButton('Include')
                    tempbutton.setMaximumSize(80, 40)
                    tempbutton.clicked.connect(self.on_button_clicked)
                    new_buttonlist.append(tempbutton)
                    self.gridLayout.addWidget(new_drugs_list[-1], count, 0)
                    self.gridLayout.addWidget(new_buttonlist[-1], count, 1)
            #self.groupBox.setMaximumHeight(count*GROUPBOX_HEIGHT)
            self.search_button.setText('Reset')
            global drugs_list
            drugs_list = new_drugs_list
            global buttonlist
            buttonlist = new_buttonlist
        else:
            self.show_all()

    def getdata(self,size):
        try:
            main= open(self.raw_database_path)
        except:
            main= open(r'C:\Users\Anil Saini\OneDrive\Desktop\College\Inventory Management System\drugs.csv')#Resorts to default database
        self.data=[]
        for i in range(size):
            temp= main.readline()
            if not temp:
                break
            final= temp.split(sep=',')
            self.data.append(final[0])

if __name__=='__main__':
    App= QApplication(sys.argv)
    window= addItems(r'C:\Users\Anil Saini\OneDrive\Desktop\College\Inventory Management System\drugs.csv')
    sys.exit(App.exec())