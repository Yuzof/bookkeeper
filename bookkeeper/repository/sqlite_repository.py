"""
Модуль описывает репозиторий, работающий в памяти постоянно запоминающего устройства.
"""

from itertools import count
from typing import Any

from bookkeeper.repository.abstract_repository import AbstractRepository, T

from inspect import get_annotations

import sqlite3

def table_types_creator(fields: dict) -> str:
    result = '('
    for key, value in fields.items():
        result += key
        if 'str' in str(value):
            result += ' TEXT'
        if 'int' in str(value):
            result += ' INTEGER'
        if 'datetime' in str(value):
            result += ' DATETIME'
        result += ', '
    return result[:-2] + ')'

class SQLiteRepository(AbstractRepository[T]):
    """
    Репозиторий, работающий в памяти постоянно запоминающего устройства.
    Хранит данные с помощью СУБД sqlite3.
    """
    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')

    def add(self, obj: T) -> int:
        names = ', '.join(self.fields.keys())
        p = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(f'CREATE TABLE IF NOT EXISTS {self.table_name} ' + table_types_creator(self.fields))
            cur.execute(f'INSERT INTO {self.table_name} ({names}) VALUES ({p})', values)
            obj.pk = cur.lastrowid
        con.close()
        return obj.pk
    
    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        if where is None:
            with sqlite3.connect(self.db_file) as con:
                cur = con.cursor()
                cur.execute('PRAGMA foreign_keys = ON')
                try:
                    cur.execute(f'SELECT rowid, * FROM {self.table_name}')
                    records = cur.fetchall()
                except sqlite3.OperationalError:
                    print('The table probably do not exist. Try to add smth first.')
                    records = list()
            con.close()
            return list(records)
        else:
            with sqlite3.connect(self.db_file) as con:
                cur = con.cursor()
                names = ', '.join(where.keys())
                values = "'" + "', '".join(where.values()) + "'"
                cur.execute('PRAGMA foreign_keys = ON')
                cur.execute(f'SELECT * FROM {self.table_name} WHERE ({names}) = ({values});')
                records = cur.fetchall()
            con.close()
            return list(records)

    def delete(self, pk: int) -> None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            try:
                cur.execute(f'DELETE FROM {self.table_name} WHERE rowid = {pk}')
            except sqlite3.OperationalError as e:
                print(e)
                print('The table probably do not exist. Try to add smth first.')
        con.close()

    def get(self, pk: int) -> T | None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            try:
                cur.execute(f'SELECT * FROM {self.table_name} WHERE rowid = {pk}')
                records = cur.fetchall()
            except sqlite3.OperationalError as e:
                print(e)
                print('The table probably do not exist. Try to add smth first.')
                records = None
        con.close()
        return records

    def update(self, pk: int, obj: T) -> None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            names = ', '.join(self.fields.keys())
            p = ', '.join("?" * len(self.fields))
            values = [getattr(obj, x) for x in self.fields]    
            try:
                cur.execute(f'UPDATE {self.table_name} SET ({names}) = ({p}) WHERE rowid = {pk}', values)
            except sqlite3.OperationalError as e:
                print(e)
                print('The table probably do not exist. Try to add smth first.')
                records = None
        con.close()
