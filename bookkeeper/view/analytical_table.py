"""
Analytical Table
It's a modular widget for the home screen in the bookkeeper application
"""
from PySide6 import QtWidgets
from bookkeeper.view.uadc_table import UADCTable
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense


class AnalyticalTable(QtWidgets.QWidget):  # pylint: disable=too-few-public-methods
    """
    Brilliant analytical table. Uses UADCTable, but some info
    gets from another table.
    """
    def __init__(self, area_repo: AbstractRepository[Budget],
                 study_repo: AbstractRepository[Expense],
                 tname: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.study_repo = study_repo
        self.area_repo = area_repo
        self.layout = QtWidgets.QVBoxLayout()
        #  budget table
        self.table = UADCTable(area_repo, tname)
        self.layout.addWidget(self.table)
        #  update calculations button
        calculate_button = QtWidgets.QPushButton('Пересчитать бюджет')
        self.layout.addWidget(calculate_button)
        calculate_button.clicked.connect(self.calc_budg)
        self.setLayout(self.layout)

    def calc_budg(self) -> None:
        """
        Calculates the budget from another table.
        """
        data = self.study_repo.get_all()
        for period in self.area_repo.get_all():
            cur_val = period
            cur_val.value = period.calculate(data)
            self.area_repo.update(cur_val)
        self.table.refresh_click()
