from flask import Flask
import json
import os


class GuiderFlask(Flask):

    def __init__(self, import_name, **kwargs):
        """
        Extension of Flask class

        Contains utility methods required by guider app

        :param import_name: import name just like in flask
        :param kwargs: flask kwargs
        """
        super().__init__(import_name, **kwargs)
        self.maps_api_key = None
        self.coords = None
        self.last_route = None
        self.request_file = os.path.join('data', 'request_log.txt')
        self.marie_parser = None

        self.load_key()
        self.load_city_coords()

    def load_key(self):
        """
        Loads api key for using google maps api into attribute maps_api_key
        """
        with open(os.path.join('static', 'config_files', 'maps_api_key.key'), 'r') as kf:
            self.maps_api_key = kf.read()

    def load_city_coords(self):
        """
        Loads coordinates for cities into attribute coords
        """
        with open(os.path.join('static', 'config_files', 'city_coordinates.json'), 'r') as cf:
            self.coords = json.load(cf)

    def city_coords(self):
        """
        Turns coords into json object usable by javascript
        :return: a javascript friendly json string that can be converted into a JSON object
        """
        return json.dumps(self.coords, separators=(',', ':'))

    def log_request(self, route):
        """
        Stores a route request in the request file
        :param route: requested route
        """
        with open(self.request_file, 'a+') as rf:
            rf.write(route + '\n')

        self.last_route = route

    def store_parsed_marie(self, parser):
        self.marie_parser = parser

