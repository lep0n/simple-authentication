import sqlite3

# from typing import Optional

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()


def fetchone(table: str, column: str, username: str) -> tuple:
    """Return one column from table."""

    cursor.execute(f"SELECT {column} FROM {table} WHERE {username=}")
    result = cursor.fetchone()
    conn.commit()

    return result


def fetchall(table: str, columns: list[str]) -> list[dict]:
    """Return dict with columns from table."""

    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    conn.commit()

    result = []

    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)

    return result


def insert(table: str, column_values: dict) -> None:
    """Insert new row in table."""

    columns = ", ".join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ", ".join("?" * len(column_values.keys()))

    cursor.executemany(
        f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", values
    )
    conn.commit()
