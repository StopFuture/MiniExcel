from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QTabWidget, QHBoxLayout, QLabel


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