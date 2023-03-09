from bookkeeper.view.MainWindow import MainWindow
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from PySide6 import QtWidgets
import sys

exp_repo_sql = SQLiteRepository[Expense]('123.db', Expense)
#print(*exp_repo_sql.get_all(), sep='\n')

app = QtWidgets.QApplication(sys.argv)
window = MainWindow(exp_repo_sql)
window.show()
app.exec()
