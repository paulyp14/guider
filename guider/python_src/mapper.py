from googlemaps.client import Client
from googlemaps.directions import directions


class DirectionBuilder:

    def __init__(self, key, route=None):
        self._client = Client(key)
        self._route = route
        self._params = None
        self.directions = None

        if route is not None:
            self._parse_route()

            self.get_directions()

    def get_directions(self):
        print('Getting directions for params:')
        print(self._params)
        self.directions = {
            'routes': directions(self._client,
                                 self._params['origin'],
                                 self._params['destination'],
                                 mode=self._params['travelmode'],
                                 waypoints=self._params['waypoints']),
            'travelmode': self._params['travelmode'].upper()
        }
        self._transform_for_renderer()

    def change_route(self, route):
        self._route = route
        self._parse_route()

    def _parse_route(self):
        def extract_params():
            chunks = self._route.split('?')[1].split('&')
            print(chunks)
            return [(chunk.split('=')[0], chunk.split('=')[1]) for chunk in chunks]

        self._params = {p: wrap_url_appropriate(p, param) for p, param in extract_params()}

    def _transform_for_renderer(self):
        if self.directions is not None:
            dir_dict = {'travelmode': self.directions['travelmode']}
            legs = self.directions['routes'][0]['legs']
            route_len = len(legs)
            if route_len == 1:
                dir_dict['start_address'] = legs[0]['start_address']
                dir_dict['end_address'] = legs[0]['end_address']
                dir_dict['waypoints'] = []
            else:
                dir_dict['start_address'] = legs[0]['start_address']
                dir_dict['end_address'] = legs[-1]['end_address']
                dir_dict['waypoints'] = [{'location': wp['end_address']} for wp in legs[0: (route_len - 1)]]
            self.directions = dir_dict



def wrap_url_appropriate(param_type, str_):
    def reverse_url_appropriate(s):
        return s.replace('%2C', ',').replace('+', ' ')

    if param_type != 'waypoints':
        return reverse_url_appropriate(str_)
    else:
        return [reverse_url_appropriate(s_) for s_ in str_.split('|')]