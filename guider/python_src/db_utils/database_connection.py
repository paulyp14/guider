import sqlite3


class DatabaseConnection:
    def __init__(self):
        self.conn = None
        self.cur = None

    def __enter__(self):
        self.conn = sqlite3.connect('database.db')
        self.cur = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()

    def _do_query(self, sql_q):
        self.cur.execute(sql_q)

    def insert(self, sql_q):
        self._do_query(sql_q)
        self.conn.commit()

    def fetch(self, sql_q):
        self._do_query(sql_q)
        return list(self.cur.fetchall())