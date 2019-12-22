from flask_login import UserMixin


class GuiderUser(UserMixin):
    def __init__(self, person_id, username, email, role, password=None):
        """
        Class for creating sessions based on user

        :param unique_id: the unique id associated with each user in the db
        :param username: the username created at sign up
        :param email: the email used at sign up
        :param password: the confirmed password at signup
        """

        self.id = email
        self.person_id = person_id
        self.username = username
        self.password = password
        self.role = role