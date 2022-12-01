
from PyQt6.QtCore import QRect
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import sys
from beautifultable import BeautifulTable
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtGui import QPalette, QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt6.QtGui import QPixmap
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys

from rich.color import Color

from TableVisual import *


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tableWidget = None
        self.setWindowTitle('MiniExcel')
        self.Width = 1000
        self.height = int(0.618 * self.Width)
        self.resize(self.Width, self.height)

        self.setMaximumHeight(1600)
        self.setMaximumWidth(2560)
        self.sheet = MyTable(10, 10)
        self.res_sheet = MyTable(10, 10)

        bar = self.menuBar()
        file = bar.addMenu('File')

        save_action = QAction('&Save', self)
        save_action.setShortcut('Ctrl+S')
        open_action = QAction('&Open', self)

        file.addAction(save_action)
        file.addAction(open_action)

        save_action.triggered.connect(self.res_sheet.save_sheet)
        open_action.triggered.connect(self.sheet.open_sheet)

        self.btn_1 = QPushButton('Editor', self)
        self.btn_2 = QPushButton('Viewer', self)
        self.btn_3 = QPushButton('Info', self)
        self.btn_4 = QPushButton('Copyright', self)

        self.btn_1.setObjectName('left_button')
        self.btn_2.setObjectName('left_button')
        self.btn_3.setObjectName('left_button')
        self.btn_4.setObjectName('left_button')

        self.btn_1.clicked.connect(self.button1)
        self.btn_2.clicked.connect(self.button2)
        self.btn_3.clicked.connect(self.button3)
        self.btn_4.clicked.connect(self.button4)

        self.btn_ui1_1 = QPushButton('Add Row', self)
        self.btn_ui1_2 = QPushButton('Add Column', self)
        self.btn_ui1_3 = QPushButton('Delete Row', self)
        self.btn_ui1_4 = QPushButton('Delete Column', self)
        self.btn_ui1_5 = QPushButton('ShowFormulas', self)

        self.btn_ui2_1 = QPushButton("Result before processing all cells", self)

        self.btn_ui1_1.clicked.connect(self.sheet.add_row)
        self.btn_ui1_2.clicked.connect(self.sheet.add_col)
        self.btn_ui1_3.clicked.connect(self.sheet.del_row)
        self.btn_ui1_4.clicked.connect(self.sheet.del_col)
        self.btn_ui1_5.clicked.connect(self.text_show)




        self.figure = plt.figure()

        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.canvas, self)

        self.lineEdit = QLineEdit()
        self.lineEdit.setText("Result after processing all cells")

        # add tabs
        self.tab1 = self.ui1()
        self.tab2 = self.ui2()
        self.tab3 = self.ui3()
        self.tab4 = self.ui4()

        self.init_ui()

    def init_ui(self):

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.btn_1)
        left_layout.addWidget(self.btn_2)
        left_layout.addWidget(self.btn_3)
        left_layout.addWidget(self.btn_4)
        left_layout.addStretch(5)
        left_layout.setSpacing(20)

        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        left_widget.setStyleSheet('''
            QPushButton{
                border:none;
                color:rgb(0,0,0);
                font-size:20px;
                font-weight:400;
                text-align:left;
            }
            QPushButton#left_button:hover{
                font-weight:600;
                background:rgb(220,220,220);
                border-left:5px solid blue;
            }
            QWidget#left_widget{
                background:rgb(220,220,220);
                border-top:1px solid white;
                border-bottom:1px solid white;
                border-left:1px solid white;
                border-top-left-radius:10px;
                border-bottom-left-radius:10px;
            }
        ''')

        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")

        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')
        self.right_widget.addTab(self.tab4, '')

        self.right_widget.setCurrentIndex(0)
        self.right_widget.setStyleSheet('''QTabBar::tab{width: 0; height: 0; margin: 0; padding: 0; border: none;}''')

        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget)
        main_layout.addWidget(self.right_widget)
        main_layout.setStretch(0, 40)
        main_layout.setStretch(1, 200)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def button1(self):
        self.right_widget.setCurrentIndex(0)
        self.clean()
        self.btn_1.setStyleSheet('''font-weight:600;background:rgb(220,220,220);''')

    def button2(self):
        self.right_widget.setCurrentIndex(1)
        self.clean()
        self.btn_2.setStyleSheet('''font-weight:600;background:rgb(220,220,220);''')

    def button3(self):
        self.right_widget.setCurrentIndex(2)
        self.clean()
        self.btn_3.setStyleSheet('''font-weight:600;background:rgb(220,220,220);''')

    def button4(self):
        self.right_widget.setCurrentIndex(3)
        self.clean()
        self.btn_4.setStyleSheet('''font-weight:600;background:rgb(220,220,220);''')

    # -----------------
    # functions

    def clean(self):
        self.btn_1.setStyleSheet('''''')
        self.btn_2.setStyleSheet('''''')
        self.btn_3.setStyleSheet('''''')
        self.btn_4.setStyleSheet('''''')

    def text_clean(self):
        self.textBox.setText('')

    def text_show(self):
        lst = self.sheet.cells
        painter = [[None for _ in range(self.sheet.columnCount())] for _ in range(self.sheet.rowCount())]
        for i in range(len(painter)):
            for j in range(len(painter[0])):
                if (i , j ) in lst:
                    painter[i][j] = str(lst[(i , j)])

        table = painter


        df = pd.DataFrame(table)
        self.res_sheet.open_n_sheet(table)


        '''
        self.textBox = str(table)
        self.showText.setText(self.textBox)
        string = str(self.textBox.toPlainText())
        for i in range(len(string)):
            self.strList = np.append(self.strList, string[i])
        self.plot()
        self.strList = np.array([])'''

    def plot(self):
        ax = self.figure.add_subplot(111)
        ax.clear()
        ax.set(xlabel="character", ylabel="frequency")
        ax.set(title="The frequency of characters")
        ax.hist(self.strList, bins=24)
        self.canvas.draw()

    # -----------------
    # pages

    def ui1(self):

        upper_layout = QHBoxLayout()
        upper_layout.addWidget(self.btn_ui1_1)
        upper_layout.addWidget(self.btn_ui1_2)
        upper_layout.addWidget(self.btn_ui1_3)
        upper_layout.addWidget(self.btn_ui1_4)
        upper_layout.addWidget(self.btn_ui1_5)

        '''
        upper_layout1 = QHBoxLayout()
        upper_layout1.addWidget(self.lineEdit)
        upper_layout1.addWidget(self.btn_ui1_1)
        upper_layout1.addWidget(self.btn_ui1_1)
        upper_layout1.addWidget(self.btn_ui1_1)
        '''
        main_layout = QVBoxLayout()
        main_layout.addLayout(upper_layout)

        main_layout.addWidget(self.sheet)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def ui2(self):
        upper_layout = QHBoxLayout()
        upper_layout.addWidget(self.btn_ui2_1)
        main_layout = QVBoxLayout()

        main_layout.addLayout(upper_layout)
        main_layout.addWidget(self.res_sheet)
        main = QWidget()
        main.setLayout(main_layout)
        main.setMaximumWidth(2560)
        main.setMaximumHeight(1600)
        return main

    def ui3(self):

        label = QLabel(self)
        pixmap = QPixmap('funct.png')
        label.setPixmap(pixmap)

        main_layout = QVBoxLayout()
        main_layout.addWidget(label)

        main = QWidget()
        main.setLayout(main_layout)
        return main

    def ui4(self):
        ui4_label1 = QLabel('Spreadsheet Imitator')
        ui4_label1.setStyleSheet('''color:white;font-size:45px;background:rgb(200,220,220);''')
        ui4_label2 = QLabel('Author: Andriy Fedorych 2022\nGitHub: StopFuture\n')
        ui4_label2.setStyleSheet('''font-size:20px;''')
        ui4_label3 = QLabel('')

        label = QLabel(self)
        pixmap = QPixmap('hehe_final.png')
        label.setPixmap(pixmap)

        footer_layout = QHBoxLayout()
        footer_layout.addStretch(5)
        footer_layout.addWidget(ui4_label3)

        main_layout = QVBoxLayout()
        main_layout.addWidget(ui4_label1)
        main_layout.addWidget(ui4_label2)
        main_layout.addStretch(10)
        main_layout.addLayout(footer_layout)
        main_layout.addWidget(label)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def fill_line(self, sheet):
        row = sheet.currentRow()
        col = sheet.currentColumn()
        thing = sheet.item(row, col)
        if thing is not None and thing.text() != '' and thing.text()[0] != '=' and thing.text()[0] != '#':
            self.lineEdit.setText(thing)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec())