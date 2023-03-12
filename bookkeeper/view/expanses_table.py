from PySide6 import QtWidgets
from PySide6.QtCore import QDateTime
from bookkeeper.view.uadc_table import UADCTable
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.models.category import Category

class ExpansesTable(UADCTable):
    def __init__(self, cat_repo: AbstractRepository[Category], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.cat_repo = cat_repo

    def add_menu(self) -> None:
        """
        Action after pressing 'Добавить'. Opens configuration menu to add
        one more element to the repository.
        """
        self.dlg = QtWidgets.QDialog()
        layout = QtWidgets.QGridLayout()
        self.dlg_widgets = []
        for i, element in enumerate(self.repo.fields):
            if element == 'category':
                self.dlg_widgets.append(QtWidgets.QComboBox())
                for categories in self.cat_repo.get_all():
                    self.dlg_widgets[-1].addItem(categories.name)
            elif 'date' in element:
                self.dlg_widgets.append(QtWidgets.QDateTimeEdit())
                self.dlg_widgets[-1].setDateTime(QDateTime.currentDateTime())
            else:
                self.dlg_widgets.append(QtWidgets.QLineEdit())
            layout.addWidget(QtWidgets.QLabel(str(element)), i, 0)
            layout.addWidget(self.dlg_widgets[-1], i, 1)
        add = QtWidgets.QPushButton('Добавить')
        cancel = QtWidgets.QPushButton('Отменить')
        cancel.clicked.connect(self.cancel)
        add.clicked.connect(self.add_click)
        layout.addWidget(add, len(self.repo.fields)+1, 0)
        layout.addWidget(cancel, len(self.repo.fields)+1, 1)
        self.dlg.setLayout(layout)
        self.dlg.setWindowTitle('Добавить покупку')
        self.dlg.exec()