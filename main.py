import pandas as pd
import sys
import datetime
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QScrollArea, QLabel, QGridLayout,QPushButton, QWidget, QGroupBox, QVBoxLayout, QLineEdit, QMenuBar, QAction, QMainWindow, QFileDialog, QSizePolicy
from FILES.addItems import addItems
from FILES.createItems import createItems
from FILES.Vendors import Vendors
from FILES.placeOrder import placeOrder
from FILES.graphs import Graphs_orders, Graphs_items
from FILES.bills import bills
from FILES.manageItems import manageItem

#self.FILE is the main database

pd.options.display.max_rows=10000
label_width=1753
GROUPBOX_HEIGHT= 50
GROUPBOX_WIDTH= 1871

class Window(QMainWindow):
    def __init__(self, mainwindow):
        self.actionCheck=0          #Checks which action has been executed through the menu
        self.call_graph_code=0          #Checks which graph is to be displayed
        self.raw_database_path=''           #The path to the raw database, on which addItems works
        self.main_database_path=''
        self.vendor_database_path=''
        super().__init__()
        self.title='Main Inventory'
        self.left= 0
        self.top= 0
        self.width= 1900
        self.height= 950

        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.status= QLabel()

        self.getdata()

        self.gridLayout= QGridLayout()
        self.gridLayout.setSpacing(10)
        self.groupBox= QGroupBox()

        self.search_button= QPushButton('Search')
        self.search_button.setMaximumHeight(30)
        self.search_button.clicked.connect(self.search)

        self.drugs_list=[]
        self.button_list=[]

        self.initialise_lists()
        self.groupBox.setLayout(self.gridLayout)
        self.scroll= QScrollArea()
        self.scroll.setWidget(self.groupBox)

        self.layout= QGridLayout()
        self.search_field= QLineEdit()
        self.search_field.setPlaceholderText('Search by Name')
        self.layout.addWidget(self.search_field,0,0,1,7)
        self.layout.addWidget(self.search_button,0,7,1,1)
        self.layout.addWidget(self.scroll,1,0,1,-1)

        self.layout.addWidget(self.status,2,0)

        self.textred= QLabel('Items with insufficient data')
        self.textred.setStyleSheet('color:red; background-color:black')
        self.textpink= QLabel('Items with zero stock')
        self.textpink.setStyleSheet('color: {}'.format(QColor(255, 204, 0).name()))

        self.black_row_widget = QWidget()
        self.black_row_widget.setAutoFillBackground(True)
        palette = self.black_row_widget.palette()
        palette.setColor(self.black_row_widget.backgroundRole(), QColor("black"))
        self.black_row_widget.setPalette(palette)

        self.layout.addWidget(self.black_row_widget, 3,0,1,-1)
        self.layout.addWidget(self.textred, 3,0)
        self.layout.addWidget(self.textpink, 3,1)

        self.refresh_button= QPushButton('Refresh')
        self.refresh_button.clicked.connect(self.addItems_database)
        self.layout.addWidget(self.refresh_button,3,7)

        self.menubar= QMenuBar()
        self.insert_item= self.menubar.addMenu('Insert Items')
        self.new_item_database= QAction('From the Database', self)
        self.insert_item.addAction(self.new_item_database)
        self.new_item_database.triggered.connect(self.call_addItems)
        self.new_item= QAction('Create a New Item', self)
        self.new_item.triggered.connect(self.call_createItems)
        self.insert_item.addAction(self.new_item)
        self.insert_item.addSeparator()
        self.new_main_database= QAction('Add a new inventory database')
        self.new_main_database.triggered.connect(self.add_new_main_database)
        self.insert_item.addAction(self.new_main_database)
        self.create_main_database= QAction('Create a new inventory database')
        self.create_main_database.triggered.connect(self.create_new_main_database)
        self.insert_item.addAction(self.create_main_database)
        self.insert_item.addSeparator()
        self.new_raw_database= QAction('Add a new raw database')
        self.new_raw_database.triggered.connect(self.create_new_raw_database)
        self.insert_item.addAction(self.new_raw_database)

        self.vendors_item= self.menubar.addMenu('Vendors')
        self.manage_vendors= QAction('Manage Vendors', self)
        self.manage_vendors.triggered.connect(self.call_Vendors)
        self.vendors_item.addAction(self.manage_vendors)
        self.order= QAction('Place Orders', self)
        self.order.triggered.connect(self.call_placeOrder)
        self.vendors_item.addAction(self.order)
        self.add_vendor_database= QAction('Add a vendor database')
        self.add_vendor_database.triggered.connect(self.add_new_vendor_database)
        self.vendors_item.addSeparator()
        self.vendors_item.addAction(self.add_vendor_database)
        self.create_vendor_database= QAction('Create a vendor database')
        self.create_vendor_database.triggered.connect(self.create_new_vendor_database)
        self.vendors_item.addAction(self.create_vendor_database)

        self.graphs_item= self.menubar.addMenu('Graphs')
        self.itemwise_graph= QAction('For Items', self)
        self.graphs_item.addAction(self.itemwise_graph)
        self.itemwise_graph.triggered.connect(self.setgraphcode_1)
        self.orderwise_graph= QAction('For Placed Orders', self)
        self.orderwise_graph.triggered.connect(self.setgraphcode_2)
        self.graphs_item.addAction(self.orderwise_graph)

        self.bills_item= self.menubar.addMenu('Bills')
        self.create_bill= QAction('Create a Bill', self)
        self.bills_item.addAction(self.create_bill)
        self.create_bill.triggered.connect(self.callCreateBill)

        self.layout.setMenuBar(self.menubar)

        widget= QWidget()
        widget.setLayout(self.layout)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        mainwindow.setCentralWidget(widget)
        mainwindow.setMinimumSize(self.width, self.height)
        mainwindow.show()

    def getdata(self):
        try:
            FILE= open('database_loc.txt','r')
            self.main_database_path= FILE.readline()
            self.main_database_path=self.main_database_path.replace('\n','')
            self.raw_database_path= FILE.readline()
            self.raw_database_path=self.raw_database_path.replace('\n','')
            self.vendor_database_path= FILE.readline()
            self.vendor_database_path= self.vendor_database_path.replace('\n','')
            FILE.close()
        except:
            self.main_database_path='mainlist.csv'
            self.raw_database_path= 'raw_database.csv'
            self.vendor_database_path='vendors.csv'
            self.write_database_path()
            
        try:
            self.FILE= pd.read_csv(self.main_database_path)
        except pd.errors.EmptyDataError:
            self.FILE= pd.DataFrame(columns=['Name','Stock','Price','UPC','HISTORY','SALES'])
            self.FILE.to_csv(self.main_database_path, index=False)
            self.status.setText('Created a new inventory database')
        except FileNotFoundError:
            self.FILE= pd.DataFrame(columns=['Name','Stock','Price','UPC','HISTORY','SALES'])
            self.main_database_path='mainlist.csv'
            self.write_database_path()
            self.FILE.to_csv(self.main_database_path, index=False)
            self.status.setText('Could not find inventory database, new one created')

        try:
            vendors= pd.read_csv(self.vendor_database_path)
        except pd.errors.EmptyDataError:
            vendors= pd.DataFrame(columns=['Name','Email','Phone','Items','Date_Added','ORDERS', 'REMARKS'])
            vendors.to_csv(self.vendor_database_path, index=False)
            self.status.setText('Created a new vendor database')
        except FileNotFoundError:
            vendors= pd.DataFrame(columns=['Name','Email','Phone','Items','Date_Added','ORDERS', 'REMARKS'])
            self.vendor_database_path='vendors.csv'
            self.write_database_path()
            vendors.to_csv(self.vendor_database_path, index=False)
            self.status.setText('Could not find vendor database, new one created')

        raw_database= open(self.raw_database_path, 'a')
        raw_database.close()

    def verify(self):
        size= self.FILE.shape
        self.FILE=pd.read_csv(self.main_database_path)
        for i in range(size[0]):
            if self.FILE.at[i, 'Price']==int(0) or self.FILE.at[i, 'Price']=='' or self.FILE.at[i, 'Price']==0.0:
                for j in range(len(self.drugs_list)):
                    if self.drugs_list[j].text()==self.FILE.at[i,'Name']:
                        self.drugs_list[j].setStyleSheet('color: red')
                        break
            elif self.FILE.at[i, 'Stock']==int(0) or self.FILE.at[i, 'Stock']=='' or self.FILE.at[i, 'Stock']==0.0:
                for j in range(len(self.drugs_list)):
                    if self.drugs_list[j].text()==self.FILE.at[i,'Name']:
                        self.drugs_list[j].setStyleSheet('color: {}'.format(QColor(255, 204, 0).name()))
                        break
            else:
                for j in range(len(self.drugs_list)):
                    if self.drugs_list[j].text()==self.FILE.at[i,'Name']:
                        self.drugs_list[j].setStyleSheet('color: black')
                        break
            

    def write_database_path(self):
        FILE= open('database_loc.txt', 'w')
        FILE.write(self.main_database_path)
        FILE.write('\n')
        FILE.write(self.raw_database_path)
        FILE.write('\n')
        FILE.write(self.vendor_database_path)
        FILE.close()

    def initialise_lists(self):
        self.drugs_list=[]
        self.button_list=[]
        size= self.FILE.shape
        self.groupBox.setMinimumHeight(size[0]*GROUPBOX_HEIGHT)
        self.groupBox.setMaximumHeight(size[0]*GROUPBOX_HEIGHT)
        if(size[0]>15):         #So that the horizontal scroll bar does not show up
            self.groupBox.setMaximumWidth(GROUPBOX_WIDTH-25) 
            self.groupBox.setMinimumWidth(GROUPBOX_WIDTH-25)
        else:
            self.groupBox.setMaximumWidth(GROUPBOX_WIDTH)
            self.groupBox.setMinimumWidth(GROUPBOX_WIDTH)
        for i in range(size[0]):
            templabel= QLabel(str(self.FILE.iloc[i][0]))
            templabel.setFixedWidth(label_width)
            templabel.setWordWrap(True)
            self.drugs_list.append(templabel)
            tempbutton= QPushButton('Manage')
            tempbutton.setMaximumSize(80,40)
            tempbutton.clicked.connect(self.on_manage_clicked)
            self.button_list.append(tempbutton)
        self.sort()
        self.search_button.setText('Search')

    def search(self):
        check= self.search_button.text()
        if check=='Search':
            key= self.search_field.text()
            new_drugs_list=[]
            new_button_list=[]
            for i in reversed(range(self.gridLayout.count())):
                self.gridLayout.itemAt(i).widget().setParent(None)
            count =0
            size= self.FILE.shape
            for i in range(size[0]):
                search_check= self.FILE.loc[i][0].find(key)
                if search_check !=-1:
                    count+=1
                    templabel= QLabel(str(self.FILE.iloc[i][0]))
                    templabel.setFixedWidth(label_width)
                    templabel.setWordWrap(True)
                    new_drugs_list.append(templabel)
                    tempbutton= QPushButton('Manage')
                    tempbutton.setMaximumSize(80,40)
                    tempbutton.clicked.connect(self.on_manage_clicked)
                    new_button_list.append(tempbutton)
                    self.gridLayout.addWidget(new_drugs_list[-1], count-1, 0)
                    self.gridLayout.addWidget(new_button_list[-1], count-1, 1)

            self.groupBox.setMinimumHeight(count*(GROUPBOX_HEIGHT))
            self.groupBox.setMaximumHeight(count*GROUPBOX_HEIGHT)
            if count>15:
                self.groupBox.setMaximumWidth(GROUPBOX_WIDTH-25)
                self.groupBox.setMinimumWidth(GROUPBOX_WIDTH-25)
            else:
                self.groupBox.setMinimumWidth(GROUPBOX_WIDTH)
                self.groupBox.setMaximumWidth(GROUPBOX_WIDTH)
            self.search_button.setText('Reset')
            self.drugs_list= new_drugs_list
            self.button_list= new_button_list
            self.verify()
        else:
            self.initialise_lists()

    def call_addItems(self):
        self.actionCheck=1
        self.addItems_window= addItems(self.raw_database_path)
        self.addItems_window.show()
    
    def call_createItems(self):
        self.actionCheck=2
        self.createItems_winow= createItems()
        self.createItems_winow.show()

    def call_Vendors(self):
        self.Vendors_window= Vendors(self.main_database_path, self.vendor_database_path)
        self.Vendors_window.show()

    def call_placeOrder(self):
        self.placeOrder_window= placeOrder(self.main_database_path, self.vendor_database_path)
        self.placeOrder_window.show()

    def create_new_raw_database(self):
        self.raw_database_path, _= QFileDialog.getOpenFileName(None, "Select file", "", "CSV Files (*.csv);;All Files (*)")
        self.write_database_path()
        self.status.setText('Added a new raw database')
        self.getdata()
        self.initialise_lists()
    
    def add_new_main_database(self):
        self.main_database_path, _= QFileDialog.getOpenFileName(None, "Select file", "", "CSV Files (*.csv);;All Files (*)")
        self.write_database_path()
        self.status.setText('Added a new inventory database')
        self.getdata()
        self.initialise_lists()

    def create_new_main_database(self):
        self.main_database_path, _= QFileDialog.getSaveFileName(self, "Save file", "", "CSV Files (*.csv)")
        if self.main_database_path:
            FILE= open(self.main_database_path,'w')
            FILE.write('')
            FILE.close()
        self.write_database_path()
        self.status.setText('Created a new inventory database')
        self.getdata()
        self.initialise_lists()

    def add_new_vendor_database(self):
        self.vendor_database_path, _= QFileDialog.getOpenFileName(None, "Select file", "", "CSV Files (*.csv);;All Files (*)")
        self.write_database_path()
        self.status.setText('Added a new vendor database')
        self.getdata()
        self.initialise_lists()

    def create_new_vendor_database(self):
        self.vendor_database_path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "CSV Files (*.csv)")
        if self.vendor_database_path:
            FILE= open(self.vendor_database_path,'w')
            FILE.write('')
            FILE.close()
        self.write_database_path()
        self.status.setText('Created a new vendor database')
        self.getdata()
        self.initialise_lists()

    def call_graphs(self):
        if self.call_graph_code==2:
            self.graph_window= Graphs_orders(self.main_database_path, self.vendor_database_path)
            self.graph_window.show()
        if self.call_graph_code==1:
            self.graph_window= Graphs_items(self.main_database_path, self.vendor_database_path)
            self.graph_window.show()

    def callCreateBill(self):
        self.createBill_window= bills(self.main_database_path, self.vendor_database_path)
        self.createBill_window.show()
        self.status.setText('Created a Bill')

    def setgraphcode_1(self):
        self.call_graph_code=1
        self.call_graphs()

    def setgraphcode_2(self):
        self.call_graph_code=2
        self.call_graphs()

    def addItems_database(self):
        if self.actionCheck==0:
            self.status.setText('Nothing to refresh!')

        if self.actionCheck==1:         #When items are added from the database
            FILE= open('addItems.csv', 'r')
            stream = str(FILE.readline())
            stream_list = [i.strip().replace(' ', '') for i in stream.split(',') if i.strip()]
            FILE.close()
            count=0
            size= self.FILE.shape
            appended=False          #To check if addItems.csv wasn't empty
            time= datetime.datetime.now()
            for i in stream_list:
                if i!=' ' and i!='':
                    new_row= pd.DataFrame({'Name': i, 'Stock': 0, 'Price': 0, 'UPC': 0, 'HISTORY': str((time.strftime('%Y-%m-%d %H:%M'),0,0))}, index=[0])
                    self.FILE = self.FILE.append(new_row, ignore_index=True)
                    count+=1
                    appended= True
            if appended==True:
                if size[0]==0:          #If a new csv file is being used
                    self.groupBox.setMinimumHeight(int(GROUPBOX_HEIGHT*count))
                    self.groupBox.setMinimumWidth(GROUPBOX_WIDTH)
                else:
                    height= self.groupBox.height()
                    self.groupBox.setMinimumHeight(int(height/size[0]*(size[0]+count)))         #Changing the groupbox's dimensions
                FILE= open('addItems.csv','w')
                FILE.write('')
                FILE.close()
                self.initialise_lists()
                temp= 'Added '+ str(count) +' Row(s)'
                self.status.setText(temp)
                self.actionCheck=0

        if self.actionCheck==2:         #When a new item is created
            FILE= open('addList.csv', 'r')
            stream= FILE.readline()
            stream_list= stream.split(',')
            size= self.FILE.shape
            time= datetime.datetime.now()
            new_row= pd.DataFrame({'Name': stream_list[0], 'Stock': stream_list[1], 'Price': stream_list[2], 'UPC': stream_list[3], 'HISTORY': str((time, stream_list[1],0))}, index=[0])
            self.FILE = self.FILE.append(new_row, ignore_index=True)
            if size[0]==0:
                self.groupBox.setMinimumHeight(int(GROUPBOX_HEIGHT))
                self.groupBox.setMinimumWidth(GROUPBOX_WIDTH)
            else:
                height= self.groupBox.height()
                self.groupBox.setMinimumHeight(int(height/size[0]*(size[0]+1)))
            FILE.close()
            FILE= open('addList.csv', 'w')
            FILE.write('')
            FILE.close()
            self.initialise_lists()
            self.status.setText('Added 1 row(s)')
            self.actionCheck=0
        if self.actionCheck==3:         #When Manage button is clicked
            self.getdata()
            self.initialise_lists()
            self.actionCheck=0

    def sort(self):
        size= self.FILE.shape
        self.FILE= self.FILE.sort_values(by='Name')
        self.FILE.to_csv(self.main_database_path, index=False)
        for i in range(0, size[0]-1):
            for j in range(0, size[0]-1-i):
                if self.drugs_list[j].text()>self.drugs_list[j+1].text():
                    temp_drug= self.drugs_list[j]
                    temp_button= self.button_list[j]

                    self.drugs_list[j]= self.drugs_list[j+1]
                    self.drugs_list[j+1]= temp_drug
                    
                    self.button_list[j]= self.button_list[j+1]
                    self.button_list[j+1]= temp_button
        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().setParent(None)
        for i in range(size[0]):
            self.gridLayout.addWidget(self.drugs_list[i], i, 0)
            self.gridLayout.addWidget(self.button_list[i], i, 1)
        self.verify()

    def on_manage_clicked(self):
        button = self.sender()
        index = self.button_list.index(button)
        item= self.drugs_list[index].text()
        self.actionCheck=3
        self.manageItem_window= manageItem(item, self.main_database_path, self.vendor_database_path)
        self.manageItem_window.show()

if __name__=='__main__':
    App= QApplication(sys.argv)
    mainwindow= QMainWindow()
    window= Window(mainwindow)
    sys.exit(App.exec())
