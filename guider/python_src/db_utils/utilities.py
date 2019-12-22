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


def get_matching_user(user_email):
    """
    A simple function that gets user info for an email
    :param user_email: the email to search the db for
    :return: the matching user's info as a tuple
    """
    return fetch("""select 
        person_id, name, email, role
        from users
        where email = '{u}'""".format(u=user_email)
    )[0]


def get_all_users():
    """
    Function to get all users from the database

    :return: a list of all users and their relevant info
    """
    cols = [c[1] for c in fetch("""PRAGMA table_info('users')""") if c[1] != 'password']
    contents = fetch("""select person_id, name, email, role from users""")

    return [[*e, ('password' if i == 0 else '****')] for i, e in enumerate([cols] + contents)]


