from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, TextAreaField, PasswordField
from wtforms.validators import InputRequired, Email

from python_src.custom_validators import *

from python_src.db_utils import utilities as dbu

class CitiesForm(FlaskForm):

    address = StringField(label='Street Address', validators=[InputRequired()])
    city = StringField(label='City')
    state = StringField(label='State')
    zip = StringField(label='Zip', validators=[InputRequired()])
    mode = RadioField(label='Route mode', choices=[('one_way', 'One Way'), ('round_trip', 'Round Trip')])
    dests = TextAreaField(label='Points of Interest', validators=[WaypointValidator()])
    dest_address = StringField(label='Street Address', validators=[ValidateOneWayAddress()])
    dest_city = StringField(label='City')
    dest_state = StringField(label='State')
    dest_zip = StringField(label='Zip', validators=[ValidateOneWayAddress()])

    # def validate_dest_address(form, field):
    #     print('Validating destination address')
    #     if form.mode.data == 'one_way':
    #         if field.data is None:
    #             raise ValidationError('You have selected a one way route. You must indicate your final destination.')

    def __str__(self):
        return '\n  '.join(['Address given:', *[f'{k}: {v}' for k, v in self.__dict__.items()], ''])

    def print(self):
        print(self.__str__())

    def handle_route(self):
        dir_base = 'https://www.google.com/maps/dir/?api=1&'
        builders = [self.get_origin, self.get_waypoints,
                    (self.get_destination if self.mode.data == 'one_way' else self.origin_as_destination),
                    self.get_travelmode]

        return f"{dir_base}{'&'.join([f() for f in builders])}"

    def get_origin(self, type_str='origin'):
        # "City Hall, New York, NY" should be converted to City+Hall%2C+New+York%2C+NY
        return f'{type_str}={self.format_address("address", "city", "state", "zip")}'

    def origin_as_destination(self):
        return self.get_origin('destination')

    def get_destination(self):
        return f'destination={self.format_address("dest_address", "dest_city", "dest_state", "dest_zip")}'

    def format_address(self, *args):
        return '%2C'.join([url_appropriate(v) for k, v in self.data.items() if k in args and v is not None and v is not ''])

    def get_waypoints(self):
        return f'waypoints={"%7C".join([url_appropriate(s) for s in self.data["dests"].split(" -- ")])}'

    def get_travelmode(self):
        return 'travelmode=walking'


def url_appropriate(s):
    return s.replace(' ', '+')


class MarieSimCode(FlaskForm):
    code = TextAreaField('MarieCode', validators=[InputRequired()])


class SignUpForm(FlaskForm):

    name = StringField('name', validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired(), Email()])
    password = PasswordField('password', validators=[InputRequired()])
    confirm = PasswordField('confirm', validators=[InputRequired(), ConfirmPasswordValidator()])
    role = RadioField('number_people', choices=[('2', 'number_people_2'), ('4', 'number_people_4'), ( '6', 'number_people_6'), ('8', 'number_people_8')])

    def set_empty_string(self):
        """
        Sets the data to be empty strings so that the form renders properly
        """
        self.name.data = ''
        self.email.data = ''
        self.password.data = ''
        self.confirm.data = ''

    def transform(self):
        """
        Transforms the input of the radio field to corresponding value
        """
        if self.role.data == '2':
            r = 'Apply'
        elif self.role.data == '4':
            r = 'Donate'
        elif self.role.data == '6':
            r = 'Follow'
        else:
            r = 'Create'
        self.role.data = r

    def insert(self):
        """
        Submits form data to the database
        """
        sql = '''INSERT INTO users (name, email, password, role)
                             VALUES ('{name}', '{email}', '{password}', '{role}')'''
        sql = sql.format(name=self.name.data,
                         email=self.email.data,
                         password=self.password.data,
                         role=self.role.data)
        dbu.insert(sql)

    def __str__(self):
        return '\n  '.join(['Input:', *[f'{k}: {v}' for k, v in self.__dict__.items()], ''])


class SignInForm(FlaskForm):

    user_id = StringField('name', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired(), ValidPassword()])

    def set_empty_string(self):
        """
        Sets the data to be empty strings so that the form renders properly
        """
        self.user_id.data = ''
        self.password.data = ''

    def __str__(self):
        return '\n  '.join(['Input:', *[f'{k}: {v}' for k, v in self.__dict__.items()], ''])