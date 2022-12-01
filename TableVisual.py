import string

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import *
import sys
import os
import csv
import parser
import copy
from MiniExcel import *


class MyTable(QTableWidget):
    def __init__(self, r, c):
        super().__init__(r, c)
        self.cells = dict() # (row,col) : value
        self.origin = dict() # (row,col) : formula
        self.dependent_on = dict() # (row,col) : set<(row,col)>

        self.line = ""
        self.check_change = True
        self.init_ui()

    def init_ui(self):

        self.cellChanged.connect(self.c_current)
        self.show()

    def parse_link(self, st, row, col):

        value = list(st)
        # print("value_parse_link:", value)
        start = -1
        finish = -1
        for i, c in enumerate(value):
            if c == "_":
                start = i+1
            if c == ")" and start != -1:
                finish = i
                break
        if start != -1 and finish != -1:
            r, c = [int(x) for x in "".join(value[start + 1:finish]).split(";")]

            r -= 1
            c -= 1
            if (row, col) in self.dependent_on:
                self.dependent_on[row, col].add((r, c))
            else:
                self.dependent_on[row, col] = set([(r, c)])
            # print(r, c, f'_({r + 1};{c + 1})')
            # print("cell = ", "0" if self.item(r, c) is None else "0" if (self.item(r, c).text()) == "" else (self.item(r, c).text()))
            repl = "0" if self.item(r, c) is None else "0" if (self.item(r, c).text()) == "" else (self.item(r, c).text())
            st = st.replace(f'_({r + 1};{c + 1})', repl)
            # print("value_parse_link2:", st)
            return [start - 1, finish,  st]
        else:
            return [-1, -1, st]

    def process(self, rw, cl, status=False):
        if status == True:
            self.origin = copy.deepcopy(self.cells)
        row = rw
        col = cl
        value = self.item(row, col)
        value = value.text()
        st = set(list(value))

        tmp = True
        if "," in st:
            value = "Invalid character"
            if status == True:
                self.cells[(self.currentRow(), self.currentColumn())] = "Invalid character"
            tmp = False
        if "_" in st and tmp:
            cnt = 0
            for _ in range(self.rowCount() * self.columnCount()):
                start, finish, res = self.parse_link(value, row, col)
                if start != -1 and finish != -1:
                    value = res
                else:
                    value = res
                    break
                cnt += 1
                if cnt == 10:
                    value = "CycleError"
                # print("value = ", value)

            # print(start, finish, res)

        st = set(list(value))
        if len(value) > 1 and tmp:

            dec = value.find("dec")
            if dec != -1:
                dec_st = dec + 4
                dec_fn = -1
                for i in range(dec_st, len(value)):
                    if value[i] == ")":
                        dec_fn = i
                        break
                value = value[:dec] + "(" + value[dec_st:dec_fn] + "-1)" + value[dec_fn + 1:]
                self.cells[(self.currentRow(), self.currentColumn())] = value
            inc = value.find("inc")
            if inc != -1:
                inc_st = inc + 4
                inc_fn = -1
                for i in range(inc_st, len(value)):
                    if value[i] == ")":
                        inc_fn = i
                        break
                value = value[:inc] + "(" + value[inc_st:inc_fn] + "+1)" + value[inc_fn + 1:]
                self.cells[(self.currentRow(), self.currentColumn())] = value


            flag = False
            for char in st:
                if char not in "1234567890. _()*+-/^":
                    flag = True

            if flag == False:
                try:
                    # print("re")
                    value = parser.calc(value, parser.ShuntingYardEvaluator)
                except:
                    value = "ParseError"

        self.origin[(row, col)] = value

        self.open_n_sheet(self.rewrite())
        if status == True:
            for rw in range(self.rowCount()):
                for cl in range(self.columnCount()):
                    self.process(rw, cl)

        # print(self.dependent_on)

    def c_current(self):
        for _ in range(1):

            if self.check_change:
                self.cells[(self.currentRow(), self.currentColumn())] = self.item(self.currentRow(), self.currentColumn()).text()

                self.process(self.currentRow(), self.currentColumn(), True)

    def rewrite(self):
        lst = self.origin
        painter = [[None for _ in range(self.columnCount())] for _ in range(self.rowCount())]
        for i in range(len(painter)):
            for j in range(len(painter[0])):
                if (i, j) in lst:
                    painter[i][j] = str(lst[(i, j)])

        table = painter
        return table

    def get_current(self):

        row = self.currentRow()
        col = self.currentColumn()
        value = self.item(row, col)
        return value

    def open_sheet(self):
        self.check_change = False
        path = QFileDialog.getOpenFileName(self, 'Open CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if path[0] != '':
            with open(path[0], newline='') as csv_file:
                self.setRowCount(0)
                self.setColumnCount(10)

                my_file = csv.reader(csv_file, dialect='excel')
                for row_data in my_file:
                    row = self.rowCount()
                    self.insertRow(row)
                    if len(row_data) > 10:
                        self.setColumnCount(len(row_data) if len(row_data) > self.columnCount() else self.columnCount())
                    for column, stuff in enumerate(row_data):

                        item = QTableWidgetItem(stuff)
                        self.setItem(row, column, item)
                        self.origin[row, column] = item.text()
                        self.cells[row, column] = item.text()
        self.check_change = True

    def open_n_sheet(self, my_file):
        self.check_change = False

        self.setRowCount(0)
        self.setColumnCount(len(my_file[0]))
        for row_data in my_file:
            row = self.rowCount()
            self.insertRow(row)
            if len(row_data) > 10:
                self.setColumnCount(len(row_data))
            for column, stuff in enumerate(row_data):
                item = QTableWidgetItem(stuff)
                self.setItem(row, column, item)

        self.check_change = True
        '''        for rw in range(self.rowCount()):
            for cl in range(self.columnCount()):
                self.process(rw, cl)
                '''

    def save_sheet(self):
        path = QFileDialog.getSaveFileName(self, 'Save CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if path[0] != '':
            with open(path[0], 'w') as csv_file:
                writer = csv.writer(csv_file, dialect='excel')
                for row in range(self.rowCount()):
                    row_data = []
                    for column in range(self.columnCount()):
                        item = self.item(row, column)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append('')
                    writer.writerow(row_data)

    def add_col(self):
        self.setColumnCount(self.columnCount() + 1)

    def add_row(self):
        self.setRowCount(self.rowCount() + 1)

    def del_row(self):

        T = True
        for i in range(self.rowCount() - 1, self.rowCount() ):
            for j in range(self.columnCount()):
                if (i, j) in self.origin.keys() and self.origin[(i,j)]!="":
                    T = False
                    break
        if T and self.rowCount() != 1:
            self.setRowCount(self.rowCount() - 1)
        else:
            # print("Stupid User")
            x = 1

    def del_col(self):
        T = True
        for i in range(self.rowCount()):
            for j in range(self.columnCount()-1, self.columnCount()):
                if (i, j) in self.origin.keys() and self.origin[(i, j)] != "":
                    T = False
                    break
        if T and self.columnCount() != 1:
            self.setColumnCount(self.columnCount() - 1)
        else:
            # print("Stupid User")
            x = 1

