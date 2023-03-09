from PySide6 import QtWidgets, QtGui 
from PySide6.QtCore import Qt, Signal, QDate, QDateTime
import sys

class ComboBox(QtWidgets.QWidget):
    def __init__(self, ltext: str, rtext: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel(ltext)
        self.combo = QtWidgets.QComboBox()
        self.combo.addItem('QComboBox')
        self.combo.addItem('2')
        self.combo.addItem('3')
        self.button = QtWidgets.QPushButton(rtext)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.combo)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)


class ExpTable(QtWidgets.QWidget):
    def __init__(self, repo, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.repo = repo

        self.layout = QtWidgets.QGridLayout()

        self.tablename = QtWidgets.QLabel('Последние расходы')
        self.layout.addWidget(self.tablename, 0, 0, 1, 1)
        self.btn = QtWidgets.QPushButton('Обновить')
        self.btn.clicked.connect(self.click)
        self.layout.addWidget(self.btn, 0, 1, 1, 1)

        self.add_btn = QtWidgets.QPushButton('Добавить')
        self.add_btn.clicked.connect(self.add_click)
        self.layout.addWidget(self.add_btn, 0, 2, 1, 1)

        self.exp_tabl = QtWidgets.QTableWidget(100, len(self.repo.fields))
        for i, element in enumerate(self.repo.names.split(',')):
            self.exp_tabl.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(element))
        self.layout.addWidget(self.exp_tabl, 1, 0, 1, 50)

        self.setLayout(self.layout)

    def click(self):
        result = self.repo.get_all()
        to_table = []
        for element in result:
            values = [getattr(element, x) for x in self.repo.fields]
            to_table.append(values)
        self.add_data(to_table)
    
    def add_click(self):
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
        
        #dateEdit.setDisplayFormat('dd.MM.yyyy')

        add = QtWidgets.QPushButton('Добавить')
        cancel = QtWidgets.QPushButton('Отменить')

        cancel.clicked.connect(self.cancel1)
        add.clicked.connect(self.add1)

        layout.addWidget(add, len(self.repo.fields)+1, 0)
        layout.addWidget(cancel, len(self.repo.fields)+1, 1)

        self.dlg.setLayout(layout)
        self.dlg.setWindowTitle('Добавить покупку')
        self.dlg.exec()

    def cancel1(self):
        self.dlg.close()

    def add1(self):
        to_table = []
        for element in self.dlg_widgets:
            if isinstance(element, QtWidgets.QDateTimeEdit):
                try:
                    to_table.append(element.dateTime().toPython())
                except AttributeError as e:
                    print(e)
            else:
                try:
                    to_table.append(int(element.text()))
                except AttributeError:
                    to_table.append(element.currentText())
                except ValueError:
                    to_table.append(element.text())

        print(to_table)
        self.repo.add(self.repo.cls(*to_table))
        self.dlg.close()


    def add_data(self, data):
        for i, row in enumerate(data):
            for j, x in enumerate(row):
                self.exp_tabl.setItem(
                    i, j,
                    QtWidgets.QTableWidgetItem(str(x))
                )

class BottomMenu(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QGridLayout()

        self.layout.addWidget(QtWidgets.QLabel('Сумма'), 0, 0)
        self.layout.addWidget(QtWidgets.QLineEdit('0'), 0, 1)
        self.layout.addWidget(QtWidgets.QLabel('Категория'), 1, 0)

        self.combo = QtWidgets.QComboBox()
        self.combo.addItem('QComboBox')
        self.combo.addItem('2')
        self.combo.addItem('3')

        self.layout.addWidget(self.combo, 1, 1)
        self.layout.addWidget(QtWidgets.QPushButton('Редактировать'), 1, 2)

        self.layout.addWidget(QtWidgets.QPushButton('Добавить'), 2, 1)

        self.setLayout(self.layout)