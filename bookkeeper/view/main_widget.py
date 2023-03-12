"""
This is Main Widget
"""
from PySide6 import QtWidgets
from bookkeeper.view.uadc_table import UADCTable
from bookkeeper.view.analytical_table import AnalyticalTable
from bookkeeper.view.expanses_table import ExpansesTable
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense


class MainWidget(QtWidgets.QWidget):  # pylint: disable=too-few-public-methods
    """
    Main Widget. Holds all other widgets. Generally,
    it's a configurable blank page.
    """
    def __init__(self, exp_bd: AbstractRepository[Expense],
                 cat_bd: AbstractRepository[Category],
                 budg_bd: AbstractRepository[Budget], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setWindowTitle('The Bookkeeper App')
        self.layout = QtWidgets.QVBoxLayout()
        # expanses table
        # self.table1 = UADCTable(exp_bd, 'Таблица расходов')
        self.table1 = ExpansesTable(cat_bd, exp_bd, 'Таблица расходов')
        self.layout.addWidget(self.table1)
        # categories table
        self.table2 = UADCTable(cat_bd, 'Таблица категорий')
        self.layout.addWidget(self.table2)
        # budget table
        self.table3 = AnalyticalTable(budg_bd, exp_bd, 'Таблица бюджетов')
        self.layout.addWidget(self.table3)
        self.setLayout(self.layout)
