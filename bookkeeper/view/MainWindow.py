from PySide6 import QtWidgets, QtGui 
from PySide6.QtCore import Qt
import sys

from bookkeeper.view.widgets import *
from bookkeeper.view.PlotWidget import PlotWidget

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, dpi=100):
        fig = Figure(dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class MainWindow(QtWidgets.QWidget):
    def __init__(self, repo1, repo2, repo3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('The Bookkeeper App')

        self.layout = QtWidgets.QVBoxLayout()

        # expanses table
        self.table1 = ExpTable(repo1, 'Таблица расходов')
        self.layout.addWidget(self.table1)

        # categories table
        self.table2 = ExpTable(repo2, 'Таблица категорий')
        self.layout.addWidget(self.table2)

        # budget table
        self.table3 = ExpTable(repo3, 'Таблица бюджеотв')
        self.layout.addWidget(self.table3)

        # graphics & info
        self.sc = PlotWidget([0,1,2,3,4], [0,1,2,3,4])
        self.layout.addWidget(self.sc)
        self.layout.addWidget(QtWidgets.QLabel())

        self.setLayout(self.layout)
