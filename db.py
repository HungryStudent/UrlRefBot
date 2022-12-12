from contextlib import closing
import sqlite3

database = "users.db"


def start():
    with closing(sqlite3.connect(database)) as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users(user_id INT PRIMARY KEY, url TEXT, number TEXT)")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS outs(id INTEGER PRIMARY KEY autoincrement, user_id INT, price INT, is_paid BOOL, card TEXT)")
        connection.commit()


def get_user(user_id):
    with closing(sqlite3.connect(database)) as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        cursor.execute("SELECT user_id, url FROM users WHERE user_id = ?", (user_id,))
        return cursor.fetchone()


def get_users():
    with closing(sqlite3.connect(database)) as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        cursor.execute("SELECT user_id, url, number FROM users")
        return cursor.fetchall()


def add_user(user_id, url, number):
    with closing(sqlite3.connect(database)) as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO users VALUES(?, ?, ?)", (user_id, url, number))
        except sqlite3.IntegrityError:
            return
        connection.commit()


def get_key(user_id):
    with closing(sqlite3.connect(database)) as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        cursor.execute("SELECT url FROM users WHERE user_id = ?", (user_id,))
        return cursor.fetchone()[0]


def get_out(out_id):
    with closing(sqlite3.connect(database)) as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        cursor.execute("SELECT user_id, price, card FROM outs WHERE id = ?", (out_id,))
        return cursor.fetchone()


def get_outs(user_id):
    with closing(sqlite3.connect(database)) as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        cursor.execute("SELECT SUM(price) FROM outs WHERE user_id = ? and is_paid = true", (user_id,))
        out = cursor.fetchone()[0]
        if out is None:
            return 0
        return out


def get_ready_outs(user_id):
    with closing(sqlite3.connect(database)) as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        cursor.execute("SELECT SUM(price) FROM outs WHERE user_id = ? and is_paid = true or is_paid = null", (user_id,))
        out = cursor.fetchone()[0]
        if out is None:
            return 0
        return out


def append_out(user_id, price, card):
    with closing(sqlite3.connect(database)) as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        cursor.execute("INSERT INTO outs(user_id, price, is_paid, card) VALUES(?, ?, NULL, ?)", (user_id, price, card))
        out_id = cursor.lastrowid
        connection.commit()
        return out_id


def change_out_status(out_id, status):
    with closing(sqlite3.connect(database)) as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        cursor.execute("UPDATE outs SET is_paid = ? WHERE id = ?", (status, out_id))
        out_id = cursor.lastrowid
        connection.commit()
