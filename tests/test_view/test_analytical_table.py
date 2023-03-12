from PySide6 import QtWidgets
from bookkeeper.view.uadc_table import UADCTable
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense
from bookkeeper.view.analytical_table import AnalyticalTable

import pytest

class Custom:
    def __init__(self, area_repo: AbstractRepository[Budget],
                    study_repo: AbstractRepository[Expense],
                    tname: str, *args, **kwargs) -> None:
        self.nnn = None

@pytest.fixture
def repo():
    return AnalyticalTable()

def test1():
    pass
