from wtforms.validators import ValidationError, Email
from python_src.db_utils import utilities as dbu


class ValidateOneWayAddress(object):
    def __init__(self, message=None):
        if not message:
            message = 'You have selected a one way route. You must indicate your final destination.'
        self.message = message

    def __call__(self, form, field):
        field.required = True
        if form.mode.data == 'one_way':
            if field.data is '':
                raise ValidationError(self.message)


class WaypointValidator(object):
    def __init__(self, message=None):
        if not message:
            message = 'You have not selected a one way route. Waypoints required.'
        self.message = message

    def __call__(self, form, field):
        if form.mode.data == 'round_trip':
            if field.data is '':
                raise ValidationError(self.message)


class ConfirmPasswordValidator(object):
    def __init__(self, message=None):
        if not message:
            message = 'The password and confirmed password do not match'
        self.message = message

    def __call__(self, form, field):
        if form.password.data != form.confirm.data:
            raise ValidationError(self.message)


class ValidUser(object):
    def __init__(self, message=None):
        """
        Validation class for user name/email

        :param message: defaults to 'Invalid user'
        """
        if not message:
            message = 'Invalid user'
        self.message = message

    def __call__(self, form, field):
        """
        Validates the field of the form
        :param form: an instance of a FlaskForm or descendant
        :param field: a field from that instance

        :return: result (list of tuples) of a query for the user
        """

        try:
            # try the input as an email
            Email().__call__(form, field)
            col = 'email'
        except ValidationError:
            # not an email
            col = 'name'
        # check db for input
        res = dbu.fetch("select {c}, password from users where {c} = '{f}'".format(c=col, f=field.data))
        if len(res) == 0:
            # input not found
            raise ValidationError(self.message)
        return res


class ValidPassword(object):
    def __init__(self, message=None):
        """
        Validation class for user password

        :param message: defaults to 'Invalid password'
        """
        if not message:
            message = 'Invalid password'
        self.message = message

    def __call__(self, form, field):
        """
        Validates the password

        :param form: an instance of a FlaskForm or descendant
        :param field: a password field from that instance

        :return:
        """
        # First validates the user and gets matches
        res = ValidUser().__call__(form, form.user_id)
        # Checks for a matching password
        if field.data not in [t[1] for t in res]:
            # No matching password
            print('Password invalid')
            raise ValidationError(self.message)
        # sign the user in
        print('Password validated')



