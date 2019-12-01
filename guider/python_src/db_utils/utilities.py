from python_src.db_utils.database_connection import DatabaseConnection

"""
Utility functions for database manipulation
"""

def insert(sql_q):
    """
    A simple insert function, creates a database object and then executes the insert query
    :param sql_q: a valid SQL query
    :return:
    """
    with DatabaseConnection() as db:
        db.insert(sql_q)


def fetch(sql_q):
    """
    A simple fetch function, creates a database object and executes the query
    :param sql_q: a valid SQL query
    :return: the result as a list
    """
    res = None
    with DatabaseConnection() as db:
        res = db.fetch(sql_q)
    return res
