from PySide6 import QtWidgets
from bookkeeper.view.UADCTable import UADCTable
from bookkeeper.view.AnalyticalTable import AnalyticalTable


class MainWidget(QtWidgets.QWidget):
    def __init__(self, exp_bd, cat_bd, budg_bd, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('The Bookkeeper App')

        self.layout = QtWidgets.QVBoxLayout()

        # expanses table
        self.table1 = UADCTable(exp_bd, 'Таблица расходов')
        self.layout.addWidget(self.table1)

        # categories table
        self.table2 = UADCTable(cat_bd, 'Таблица категорий')
        self.layout.addWidget(self.table2)

        # budget table
        self.table3 = AnalyticalTable(budg_bd, exp_bd, 'Таблица бюджетов')
        self.layout.addWidget(self.table3)

        self.setLayout(self.layout)
