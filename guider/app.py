from flask import Flask
from flask import render_template, request
from datetime import datetime
import os

maps_api_key = ''

import forms

app = Flask(__name__)

app.secret_key = '123'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/cities', methods=['GET', 'POST'])
def cities(route=None):
    target = ''
    city_form = forms.CitiesForm()
    if city_form.is_submitted():
        route = city_form.handle_route()
        target = '_blank'
        print(route)
    else:
        route = '#'

    return render_template('cities.html', form=city_form, route=route, target=target)


@app.route('/handle_route', methods=['POST'])
def handle_route():
    pass


@app.route('/the_idea')
def the_idea():
    return render_template('the_idea.html')


@app.route('/test_form')
def test_form():
    city_form = forms.CitiesForm()
    return render_template('test_form.html', form=city_form)



if __name__ == '__main__':
    os.remove("data\\test.txt")
    app.run(host='0.0.0.0')
