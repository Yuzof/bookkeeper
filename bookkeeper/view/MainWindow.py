from PySide6 import QtWidgets, QtGui 
from PySide6.QtCore import Qt
import sys

from bookkeeper.view.vidgets import *


class MainWindow(QtWidgets.QWidget):
    def __init__(self, repo1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('The Bookkeeper App')

        self.layout = QtWidgets.QVBoxLayout()

        # expanses table
        self.table1 = ExpTable(repo1)
        self.layout.addWidget(self.table1)

        # budget table
        self.tablename2 = QtWidgets.QLabel('Бюджет')
        self.layout.addWidget(self.tablename2)
        self.budg_tabl = QtWidgets.QTableWidget(2, 2)
        self.layout.addWidget(self.budg_tabl)

        self.bot_menu = BottomMenu()
        self.layout.addWidget(self.bot_menu)

        self.setLayout(self.layout)
