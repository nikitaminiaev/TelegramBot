import os
from typing import Dict, List, Tuple
from parser import Parser
import sqlite3

EMPTY = 0
NANO = 1
AI = 2

# todo переделать структуру таблицы
conn = sqlite3.connect(os.path.join("db", "database.db"))
cursor = conn.cursor()


def insert(table: str, column_values: Dict):
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ", ".join("?" * len(column_values.keys()))
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()


def update(table: str, id_where: str, column_values: Dict):
    column_values_str = str(column_values).replace('{', '').replace('}', '').replace(':', '=').replace('\'', '')
    cursor.execute(
        f"UPDATE {table} "
        f"SET {column_values_str} "
        f"WHERE id = {id_where}"
    )
    conn.commit()


def isset_user(id: str):
    cursor.execute(f"SELECT id FROM users WHERE id = {id}")
    return bool(len(cursor.fetchall()))


def is_news_unique(news: str):
    cursor.execute(f"SELECT data FROM links WHERE data = '{news}'")
    return not bool(len(cursor.fetchall()))


def get_user():
    pass


def get_last_news():
    pass


def update_news(type, data):
    link = Parser.MAPPING[type]
    pass


if __name__ == '__main__':
    # insert('users', {'id': 532510956})
    # update('users', '532510956', {'subscriptions_nano': 0, 'subscriptions_ai': 0})
    print(isset_user(str(532510956)))
    # print(str(532510956))
    # insert('links', {'link': 'http://ldcn-mechatronics.net/publications/', 'is_' + 'nano': 1})
