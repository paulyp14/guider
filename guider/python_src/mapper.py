from googlemaps.client import Client
from googlemaps.directions import directions


class DirectionBuilder:

    def __init__(self, key, route=None):
        """
        A class for parsing the directions built by the CitiesForm, getting a valid route and then tranforming that route
        so it can be re-rendered by the javascript maps api

        :param key: a google maps api secret access key
        :param route: the route from the CitiesForm
        """
        self._client = Client(key)
        self._route = route
        self._params = None
        self.directions = None

        if route is not None:
            self._parse_route()

            self.get_directions()

    def get_directions(self):
        """

        Makes a request to the python maps api, then transforms the result for the javascript maps api

        """
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
        """

        Parses the route submitted by the CitiesForm

        """
        def extract_params():
            chunks = self._route.split('?')[1].split('&')
            print(chunks)
            return [(chunk.split('=')[0], chunk.split('=')[1]) for chunk in chunks]

        self._params = {p: wrap_url_appropriate(p, param) for p, param in extract_params()}

    def _transform_for_renderer(self):
        """

        Transforms python maps api directions into a usable JSON object for javascript maps api

        """
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
            self.directions = {'directions': dir_dict,
                               'dest_list': [dir_dict['start_address'],
                                             *[wp['location'] for wp in dir_dict['waypoints']],
                                             dir_dict['end_address']]
                               }


def wrap_url_appropriate(param_type, str_):
    """
    Utility function that makes a str parameter usable

    :param param_type: the maps parameter type
    :param str_: the actual parameter
    :return: usable parameter
    """
    def reverse_url_appropriate(s):
        return s.replace('%2C', ',').replace('+', ' ')

    if param_type != 'waypoints':
        return reverse_url_appropriate(str_)
    else:
        return [reverse_url_appropriate(s_) for s_ in str_.split('|')]