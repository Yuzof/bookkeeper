"""
UADC Table stands for UpdateAddDeleteChange Table.
"""

from PySide6 import QtWidgets
from PySide6.QtCore import QDateTime
from bookkeeper.repository.abstract_repository import AbstractRepository, T


class UADCTable(QtWidgets.QWidget):  # type: ignore
    """
    UADC TABLE.
    A simple table that implements the buttons of an abstract repository.
    """
    # pylint: disable=too-many-instance-attributes
    # All arguments are reasonable in this case.

    def __init__(self, repo: AbstractRepository[T],
                 tablename: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.repo = repo
        self.layout = QtWidgets.QGridLayout()

        self.tablename = QtWidgets.QLabel(tablename)
        self.layout.addWidget(self.tablename, 0, 0, 1, 1)
        self.btn = QtWidgets.QPushButton('Обновить')
        self.btn.clicked.connect(self.refresh_click)
        self.layout.addWidget(self.btn, 0, 1, 1, 1)

        self.add_btn = QtWidgets.QPushButton('Добавить')
        self.add_btn.clicked.connect(self.add_menu)
        self.layout.addWidget(self.add_btn, 0, 2, 1, 1)

        self.delete_btn = QtWidgets.QPushButton('Удалить')
        self.delete_btn.clicked.connect(self.del_menu)
        self.layout.addWidget(self.delete_btn, 0, 3, 1, 1)

        self.upd_btn = QtWidgets.QPushButton('Исправить')
        self.upd_btn.clicked.connect(self.upd_menu)
        self.layout.addWidget(self.upd_btn, 0, 4, 1, 1)
        try:
            self.exp_tabl = QtWidgets.QTableWidget(20, len(self.repo.fields) + 1)
            names = ', '.join(self.repo.fields.keys())
            for i, element in enumerate(names.split(',')):
                self.exp_tabl.setHorizontalHeaderItem(
                    i, QtWidgets.QTableWidgetItem(element)
                )
            self.exp_tabl.setHorizontalHeaderItem(
                len(self.repo.fields),
                QtWidgets.QTableWidgetItem('PK')
            )
            self.layout.addWidget(self.exp_tabl, 1, 0, 1, 50)
            self.setLayout(self.layout)
        except AttributeError as err:
            print('Error parsing DB attributes, cannot contionue.', err)
        self.dlg = QtWidgets.QDialog()
        self.dlg_widgets = []

    def refresh_click(self) -> None:
        """
        Action after pressing 'Обновить'. Makes get_all from repo and
        refreshes the table.
        """
        result = self.repo.get_all()
        to_table = []
        for element in result:
            values = [getattr(element, x) for x in self.repo.fields]
            values.append(getattr(element, 'pk'))
            to_table.append(values)
        self.exp_tabl.clearContents()
        self.add_data(to_table)

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
                self.set_categories()
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
        self.dlg.setWindowTitle('Добавить запись')
        self.dlg.exec()

    def set_categories(self) -> None:
        """
        Sets expanse categories, if they are.
        """
        self.dlg_widgets[-1].addItem('книги')
        self.dlg_widgets[-1].addItem('мясо')
        self.dlg_widgets[-1].addItem('одежда')
        self.dlg_widgets[-1].addItem('сырое мясо')
        self.dlg_widgets[-1].addItem('сладости')

    def cancel(self) -> None:
        """
        Action after pressing 'Отменить' in additional
        dialog boxes.
        """
        self.dlg.close()

    def add_click(self) -> None:
        """
        Action after pressing 'Добавить' in the additional dialog window.
        submitting the new element to the repository.
        """
        to_table = []
        for element in self.dlg_widgets:
            if isinstance(element, QtWidgets.QDateTimeEdit):
                try:
                    to_table.append(element.dateTime().toPython())
                except AttributeError as err:
                    print(err)
            else:
                try:
                    to_table.append(int(element.text()))
                except AttributeError:
                    to_table.append(element.currentText())
                except ValueError:
                    to_table.append(element.text())
        self.repo.add(self.repo.cls(*to_table))
        self.refresh_click()
        self.dlg.close()

    def del_menu(self) -> None:
        """
        Action after pressing the 'Удалить' button.
        Opens an additional comfiguration menu.
        """
        self.dlg = QtWidgets.QDialog()
        self.dlg_widgets = []
        layout = QtWidgets.QGridLayout()
        self.dlg_widgets.append(QtWidgets.QLabel('PK'))
        layout.addWidget(self.dlg_widgets[-1], 0, 0)
        self.dlg_widgets.append(QtWidgets.QLineEdit())
        layout.addWidget(self.dlg_widgets[-1], 0, 1)
        add = QtWidgets.QPushButton('Применить')
        cancel = QtWidgets.QPushButton('Отменить')
        cancel.clicked.connect(self.cancel)
        add.clicked.connect(self.del_click)
        layout.addWidget(add, 1, 0)
        layout.addWidget(cancel, 1, 1)
        self.dlg.setLayout(layout)
        self.dlg.setWindowTitle('Удалить запись')
        self.dlg.exec()

    def del_click(self) -> None:
        """
        Action after pressing the 'Удалить' button in
        additional configuration menu.
        Deletes the element with given pk from the repository.
        """
        try:
            self.repo.delete(int(self.dlg_widgets[-1].text()))
        except AttributeError as err:
            print('Unable to delete object')
            print(err)
        finally:
            self.refresh_click()
            self.dlg.close()

    def upd_menu(self) -> None:
        """
        Action after pressing 'Исправить' button.
        Opens an additional configuration menu.
        """
        self.dlg = QtWidgets.QDialog()
        layout = QtWidgets.QGridLayout()
        self.dlg_widgets = []
        for i, element in enumerate(self.repo.fields):
            if element == 'category':
                self.dlg_widgets.append(QtWidgets.QComboBox())
                self.dlg_widgets[-1].addItem('книги')
                self.dlg_widgets[-1].addItem('мясо')
                self.dlg_widgets[-1].addItem('одежда')
                self.dlg_widgets[-1].addItem('сырое мясо')
                self.dlg_widgets[-1].addItem('сладости')
            elif 'date' in element:
                self.dlg_widgets.append(QtWidgets.QDateTimeEdit())
                self.dlg_widgets[-1].setDateTime(QDateTime.currentDateTime())
            else:
                self.dlg_widgets.append(QtWidgets.QLineEdit())
            layout.addWidget(QtWidgets.QLabel(str(element)), i, 0)
            layout.addWidget(self.dlg_widgets[-1], i, 1)
        self.dlg_widgets.append(QtWidgets.QLineEdit())
        layout.addWidget(QtWidgets.QLabel('PK'), len(self.repo.fields), 0)
        layout.addWidget(self.dlg_widgets[-1], len(self.repo.fields), 1)
        add = QtWidgets.QPushButton('Исправить')
        cancel = QtWidgets.QPushButton('Отменить')
        cancel.clicked.connect(self.cancel)
        add.clicked.connect(self.upd_click)
        layout.addWidget(add, len(self.repo.fields)+1, 0)
        layout.addWidget(cancel, len(self.repo.fields)+1, 1)
        self.dlg.setLayout(layout)
        self.dlg.setWindowTitle('Исправить запись')
        self.dlg.exec()

    def upd_click(self) -> None:
        """
        Action after pressing 'Исправить' in the additional
        configuration window. Submits the results to the
        repository.
        """
        to_table = []
        for element in self.dlg_widgets:
            if isinstance(element, QtWidgets.QDateTimeEdit):
                try:
                    to_table.append(element.dateTime().toPython())
                except AttributeError as err:
                    print(err)
            else:
                try:
                    to_table.append(int(element.text()))
                except AttributeError:
                    to_table.append(element.currentText())
                except ValueError:
                    to_table.append(element.text())
        tmp = self.repo.cls(*to_table)
        print(to_table)
        print(tmp)
        self.repo.update(self.repo.cls(*to_table))
        self.refresh_click()
        self.dlg.close()

    def add_data(self, data: list) -> None:
        """
        Additional function to fill the table widget with
        new elements.
        """
        for inum, row in enumerate(data):
            for jnum, x in enumerate(row):
                self.exp_tabl.setItem(
                    inum, jnum,
                    QtWidgets.QTableWidgetItem(str(x))
                )
