from PySide6 import QtWidgets
from LabeledInput import LableledInput


class XYInput(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.x_input = LableledInput('x:', '0')
        self.y_input = LableledInput('y:', '0')
        self.submit_button = QtWidgets.QPushButton('Send')
        self.submit_button.clicked.connect(self.submit)

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.x_input)
        self.vbox.addWidget(self.y_input)
        self.vbox.addWidget(self.submit_button)
        self.setLayout(self.vbox)

    def submit(self):
        print(self.x_input.text(), self.y_input.text())