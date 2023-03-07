from PySide6 import QtWidgets

class LableledInput(QtWidgets.QWidget):
    def __init__(self, text: str, placeholder, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel(text)
        self.input = QtWidgets.QLineEdit(placeholder)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)

        self.setLayout(self.layout)

    def text(self):
        return self.input.text()