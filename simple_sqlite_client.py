"""
Простой тестовый скрипт для терминала
"""

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.utils import read_tree


cat_repo_sql = SQLiteRepository[Category]('123.db', Category)
exp_repo_sql = SQLiteRepository[Expense]('123.db', Expense)


cats = '''
продукты
    мясо
        сырое мясо
        мясные продукты
    сладости
книги
одежда
'''.splitlines()

Category.create_from_tree(read_tree(cats), cat_repo_sql)

while True:
    try:
        cmd = input('$> ')
    except EOFError:
        break
    if not cmd:
        continue
    if cmd == 'categories':
        print(*cat_repo_sql.get_all(), sep='\n')
    elif cmd == 'expanses':
        print(*exp_repo_sql.get_all(), sep='\n')
    elif cmd == 'delete expanse':
        print(*exp_repo_sql.get_all(), sep='\n')
        cmd1 = int(input('введите id записи для удаления $> '))
        exp_repo_sql.delete(cmd1)

    elif cmd == 'delete category':
        print(*cat_repo_sql.get_all(), sep='\n')
        cmd1 = int(input('введите id записи для удаления $> '))
        cat_repo_sql.delete(cmd1)
    
    elif cmd == 'about category':
        print(*cat_repo_sql.get_all(), sep='\n')
        cmd1 = int(input('введите id записи для получения информации $> '))
        print(cat_repo_sql.get(cmd1))

    elif cmd == 'about expanse':
        print(*exp_repo_sql.get_all(), sep='\n')
        cmd1 = int(input('введите id записи для получения информации $> '))
        print(exp_repo_sql.get(cmd1))

    elif cmd == 'update expanse':
        print(*exp_repo_sql.get_all(), sep='\n')
        cmd1 = int(input('введите id записи для обновления $> '))
        print(exp_repo_sql.get(cmd1))
        cmd2 = input('введите новую запись $> ')
        amount, name = cmd2.split()
        try:
            cat = cat_repo_sql.get_all({'name': name})[0]
            print(cat)
        except IndexError:
            print(f'категория {name} не найдена')
            continue
        exp = Expense(int(amount), cat[0])
        exp_repo_sql.update(cmd1, exp)

    elif cmd == 'update category':
        print(*cat_repo_sql.get_all(), sep='\n')
        cmd1 = int(input('введите id записи для обновления $> '))
        print(cat_repo_sql.get(cmd1))
        cmd2 = input('введите новую запись $> ')
        name, parent = cmd2.split()
        cat = Category(name, parent)
        cat_repo_sql.update(cmd1, cat)

    elif cmd[0].isdecimal():
        amount, name = cmd.split(maxsplit=1)
        try:
            cat = cat_repo_sql.get_all({'name': name})[0]
            print(cat)
        except IndexError:
            print(f'категория {name} не найдена')
            continue
        exp = Expense(int(amount), cat[0])
        exp_repo_sql.add(exp)
        print(exp)