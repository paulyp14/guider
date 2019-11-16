from wtforms.validators import ValidationError


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
