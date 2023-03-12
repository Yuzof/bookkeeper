"""
Special table for analysing expanses. Inheritated from UADCTable,
but categories are auto-filled. For that purpose, new class is necessery.
"""
from bookkeeper.view.uadc_table import UADCTable
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.models.category import Category


class ExpansesTable(UADCTable):
    """
    General UADCTable, but in add_menu categories from another bd
    are autofilled.
    """
    def __init__(self, cat_repo: AbstractRepository[Category], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.cat_repo = cat_repo

    def set_categories(self) -> None:
        for categories in self.cat_repo.get_all():
            self.dlg_widgets[-1].addItem(categories.name)
