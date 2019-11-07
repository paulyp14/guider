from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, TextAreaField, SubmitField
from wtforms.validators import InputRequired


class CitiesForm(FlaskForm):

    street = StringField(label='Street Address', validators=[InputRequired()])
    city = StringField(label='City')
    state = StringField(label='State')
    zip = StringField(label='Zip', validators=[InputRequired()])
    mode = RadioField(label='Route mode', choices=[('one_way', 'One Way'), ('round_trip', 'Round Trip')])
    dests = TextAreaField(label='Points of Interest', validators=[InputRequired()])

    def print(self):
        print('\n  '.join(['Address given:', *[f'{k}: {v}' for k, v in self.__dict__.items()]]))
