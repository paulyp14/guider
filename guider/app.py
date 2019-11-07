from flask import Flask
from flask import render_template, request

import forms

app = Flask(__name__)

app.secret_key = '123'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/cities', methods=['GET', 'POST'])
def cities():
    return render_template('cities.html')


@app.route('/the_idea')
def the_idea():
    return render_template('the_idea.html')


@app.route('/test_form')
def test_form():
    city_form = forms.CitiesForm()
    city_form.print()
    return render_template('test_form.html', form=city_form)



if __name__ == '__main__':
    app.run(host='0.0.0.0')
