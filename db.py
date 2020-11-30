import os
from typing import Dict, List, Tuple

import sqlite3

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

def isset_user(id):
    cursor.execute(f"SELECT id FROM users WHERE id = {id}")
    return bool(len(cursor.fetchall()))

if __name__ == '__main__':
    # insert('users', {'id': 532510956})
    isset_user(532510956)
