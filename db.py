from contextlib import closing
import sqlite3

database = "users.db"


def start():
    with closing(sqlite3.connect(database)) as connection:
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users(user_id INT PRIMARY KEY, url TEXT, number TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS outs(user_id INT, price INT)")
        connection.commit()


def get_user(user_id):
    with closing(sqlite3.connect(database)) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT user_id, url FROM users WHERE user_id = ?", (user_id,))
        return cursor.fetchone()


def get_users():
    with closing(sqlite3.connect(database)) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT user_id, url, number FROM users")
        return cursor.fetchall()


def add_user(user_id, url, number):
    with closing(sqlite3.connect(database)) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO users VALUES(?, ?, ?)", (user_id, url, number))
        except sqlite3.IntegrityError:
            return
        connection.commit()


def get_key(user_id):
    with closing(sqlite3.connect(database)) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT url FROM users WHERE user_id = ?", (user_id,))
        return cursor.fetchone()[0]


def get_outs(user_id):
    with closing(sqlite3.connect(database)) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT SUM(price) FROM outs WHERE user_id = ?", (user_id,))
        out = cursor.fetchone()[0]
        if out is None:
            return 0
        return out


def append_out(user_id, price):
    with closing(sqlite3.connect(database)) as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO outs VALUES(?, ?)", (user_id, price))
        connection.commit()
