from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, TextAreaField, SubmitField
from wtforms.validators import InputRequired


class CitiesForm(FlaskForm):

    address = StringField(label='Street Address', validators=[InputRequired()])
    city = StringField(label='City')
    state = StringField(label='State')
    zip = StringField(label='Zip', validators=[InputRequired()])
    mode = RadioField(label='Route mode', choices=[('one_way', 'One Way'), ('round_trip', 'Round Trip')])
    dests = TextAreaField(label='Points of Interest', validators=[InputRequired()])
    dest_address = StringField(label='Street Address', validators=[InputRequired()])
    dest_city = StringField(label='City')
    dest_state = StringField(label='State')
    dest_zip = StringField(label='Zip', validators=[InputRequired()])

    def __str__(self):
        return '\n  '.join(['Address given:', *[f'{k}: {v}' for k, v in self.__dict__.items()], ''])

    def print(self):
        print(self.__str__())

    def handle_route(self):
        dir_base = 'https://www.google.com/maps/dir/?api=1&'
        builders = [self.get_origin, self.get_waypoints, self.get_destination, self.get_travelmode]

        if self.data['mode'] != 'round_trip':
            splits = self.dests.data.split(',')
            if len(splits) == 1:
                self.dests.data = ''
            elif len(splits) == 2:
                self.dests.data = ','.join(splits[0:-1])
            else:
                self.dests.data = ','.join(splits[0:-1])
            self.dest_address.data = splits[-1].strip()

        maps_url = f'{dir_base}{"&".join([f() for f in builders])}'
        self.dests.data = ','.join(splits)
        return maps_url

    def get_origin(self):
        # "City Hall, New York, NY" should be converted to City+Hall%2C+New+York%2C+NY
        return f'origin={self.format_address("address", "city", "state", "zip")}'

    def get_destination(self):
        return f'destination={self.format_address("dest_address", "dest_city", "dest_state", "dest_zip")}'

    def format_address(self, *args):
        return '%2C'.join([url_appropriate(v) for k, v in self.data.items() if k in args and v is not None and v is not ''])

    def get_waypoints(self):
        return f'waypoints={"%7C".join([url_appropriate(s) for s in self.data["dests"].split(",")])}'

    def get_travelmode(self):
        return 'travelmode=walking'


def url_appropriate(s):
    return s.replace(' ', '+')
