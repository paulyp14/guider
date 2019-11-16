from python_src.db_utils.database_connection import DatabaseConnection


def insert(sql_q):
    with DatabaseConnection() as db:
        db.insert(sql_q)


def fetch(sql_q):
    res = None
    with DatabaseConnection() as db:
        res = db.fetch(sql_q)
    return res