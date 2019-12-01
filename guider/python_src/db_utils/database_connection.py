import sqlite3
from config import DB_CONNECTION

class DatabaseConnection:
    """
    Utility class for accessing the website's database
    """
    def __init__(self):
        self.conn = None
        self.cur = None

    def __enter__(self):
        self.conn = sqlite3.connect(DB_CONNECTION)
        self.cur = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()

    def _do_query(self, sql_q):
        """
        Simple function to do a query
        :param sql_q: a valid SQL query
        :return:
        """
        self.cur.execute(sql_q)

    def insert(self, sql_q):
        """
        Simple function to insert into the database
        :param sql_q: a valid SQL query
        :return:
        """
        self._do_query(sql_q)
        self.conn.commit()

    def fetch(self, sql_q):
        """
        Simple function to fetch from the database
        :param sql_q: A valid SQL query
        :return: the results as a list
        """
        self._do_query(sql_q)
        return list(self.cur.fetchall())