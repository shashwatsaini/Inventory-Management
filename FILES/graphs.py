import matplotlib
import numpy as np
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import pandas as pd
import sys
import re
import datetime
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QEventLoop, Qt
from PyQt5.QtWidgets import QApplication, QScrollArea, QLabel, QGridLayout,QPushButton, QWidget, QGroupBox, QVBoxLayout, QLineEdit, QMenuBar, QAction, QMainWindow, QFileDialog, QSizePolicy, QComboBox

class Graphs_orders(QWidget):

    def __init__(self, main_database_path, vendor_database_path):

        super().__init__()
        self.main_database_path= main_database_path
        self.vendor_database_path= vendor_database_path

        self.title= 'Graphs for Orders'
        self.left=0
        self.top=0
        self.width=1200
        self.height=700

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.layout= QGridLayout()
        self.choose_field= QComboBox()
        self.choose_field.currentIndexChanged.connect(self.display_graph)

        self.fig= Figure()
        self.plot= self.fig.add_subplot(111)
        self.canvas= FigureCanvasQTAgg(self.fig)

        self.getdata()

        self.layout.addWidget(self.choose_field,0,0)
        self.layout.addWidget(self.canvas,1,0,-1,-1)
        self.setLayout(self.layout)
        self.show()
    
    def getdata(self):
        self.FILE= pd.read_csv(self.main_database_path)
        size= self.FILE.shape
        for i in range(size[0]):
            self.choose_field.addItem(str(self.FILE.iloc[i][0]))

    def display_graph(self):
        x=[]
        y=[]
        size= self.FILE.shape
        index=-1
        for i in range(size[0]):
            if self.FILE.iloc[i][0]==self.choose_field.currentText():
                index=i
                break
        unformatted= self.FILE.iloc[index][4]
        regex= r'\((.*?)\)'
        formatted= re.findall(regex, unformatted)
        max_y=-1
        for i in formatted:
            temp_list= i.split(',')
            temp_x= str(temp_list[0])
            x.append(temp_list[0])
            y.append(int(temp_list[1]))
            if int(temp_list[1])>max_y:
                max_y= int(temp_list[1])
        self.plot.clear()
        self.plot.plot(x,y)
        self.plot.set_xlabel('Date/Time')
        self.plot.set_ylabel('Orders- Quantity')
        self.plot.set_yticks(np.arange(0, max_y + 1, 5))
        self.canvas.draw()

class Graphs_items(QWidget):
    def __init__(self, main_database_path, vendor_database_path):
        super().__init__()
        self.main_database_path= main_database_path
        self.vendor_database_path= vendor_database_path

        self.title= 'Graphs for Items'
        self.left=0
        self.top=0
        self.width=1200
        self.height=700

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.layout= QGridLayout()
        self.choose_field= QComboBox()
        self.choose_field.currentIndexChanged.connect(self.display_graph)

        self.fig= Figure()
        self.plot= self.fig.add_subplot(111)
        self.canvas= FigureCanvasQTAgg(self.fig)

        self.getdata()

        self.layout.addWidget(self.choose_field,0,0)
        self.layout.addWidget(self.canvas,1,0,-1,-1)
        self.setLayout(self.layout)
        self.show()

    def getdata(self):
        self.FILE= pd.read_csv(self.main_database_path)
        size= self.FILE.shape
        for i in range(size[0]):
            self.choose_field.addItem(str(self.FILE.iloc[i][0]))

    def display_graph(self):
        x=[]
        y=[]
        size= self.FILE.shape
        index=-1
        for i in range(size[0]):
            if self.FILE.iloc[i][0]==self.choose_field.currentText():
                index=i
                break
        unformatted= self.FILE.iloc[index][5]
        y= re.findall(r'\((?:[^),]*,)?(\d+)\)', unformatted)
        y= [int(i) for i in y]
        x= re.findall(r"\d{4}-\d{2}-\d{2}", unformatted)
        max_y=-1
        for i in range(len(y)):
            if y[i]>max_y:
                max_y= y[i]
        self.plot.clear()
        self.plot.plot(x,y)
        self.plot.set_xlabel('Date/Time')
        self.plot.set_ylabel('Orders- Quantity')
        self.plot.set_yticks(np.arange(0, max_y + 1, 5))
        self.canvas.draw()


if __name__=='__main__':
    App= QApplication(sys.argv)
    window= Graphs_items('mainlist.csv', 'vendors.csv')
    sys.exit(App.exec())
