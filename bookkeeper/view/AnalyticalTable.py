from PySide6 import QtWidgets
from bookkeeper.view.UADCTable import UADCTable


class AnalyticalTable(QtWidgets.QWidget):
    def __init__(self, areaRepo, studyRepo, tname : str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.studyRepo = studyRepo
        self.areaRepo = areaRepo
        self.layout = QtWidgets.QVBoxLayout()
        #  budget table
        self.table3 = UADCTable(areaRepo, tname)
        self.layout.addWidget(self.table3)
        #  update calculations button
        calculate_button = QtWidgets.QPushButton('Пересчитать бюджет')
        self.layout.addWidget(calculate_button)
        calculate_button.clicked.connect(self.calc_budg)
        self.setLayout(self.layout)

    def calc_budg(self) -> None:
        data = self.studyRepo.get_all()
        for period in self.areaRepo.get_all():
            curVal = period
            curVal.value = period.calculate(data)
            self.areaRepo.update(curVal)
        self.table3.refresh_click()