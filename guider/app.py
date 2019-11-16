from flask import request, jsonify
from flask import render_template, redirect, url_for
import time

from python_src import forms
from python_src.guider_flask import GuiderFlask
from python_src.mapper import DirectionBuilder
from python_src.db_utils.utilities import *

from python_src.msim.marie_parser import Parser


app = GuiderFlask(__name__)
app.secret_key = 'allo'


@app.route('/')
def home():
    return render_template('home.html', active_page='home')


@app.route('/cities', methods=['GET', 'POST'])
def cities():
    # decls
    map_route, target, trigger = '', '', False
    city_form = forms.CitiesForm()
    # if called from redirect, get the route and target
    for p in ['route', 'target', 'trigger']:
        if p in request.args.keys():
            if p == 'route':
                map_route = request.args[p]
            elif p == 'target':
                target = request.args[p]
            elif p == 'trigger':
                trigger = True
    trigger = '' if not trigger else 'load_trigger'
    # if form was submitted, use redirect
    if city_form.validate_on_submit():
        # extract route from form, allow route to be opened in new page
        map_route = city_form.handle_route()
        app.log_request(map_route)
        target = '_blank'
        # redirect
        return redirect(url_for('cities', route=map_route, target=target, trigger='True'))
    # render cities page
    return render_template('cities.html',
                           form=city_form,
                           route=map_route,
                           target=target,
                           maps_key=app.maps_api_key,
                           active_page='cities',
                           city_coords=app.coords,
                           load_trigger=trigger)


@app.route('/handle_route', methods=['GET'])
def handle_route():
    print('Handling route')
    # method to handle completing the route
    time.sleep(5)
    dir_build = DirectionBuilder(app.maps_api_key, app.last_route)
    return jsonify(dir_build.directions)


@app.route('/the_idea')
def the_idea():
    return render_template('the_idea.html', active_page='the_idea')


@app.route('/about_us/render_marie', methods=['GET', 'POST'])
def marie_form():
    mform = forms.MarieSimCode()

    if mform.validate_on_submit():
        parser = Parser(mform.code.data)
        app.store_parsed_marie(parser)
        return redirect(url_for("display_marie"))
    return render_template("msim_submit.html", form=mform, active_page='about_us')


@app.route("/about_us/rendered_marie")
def display_marie():
    return render_template("msim_rendered.html",
                           active_page='about_us',
                           rendered_code=app.marie_parser.render_html(),
                           rendered_lines=app.marie_parser.html_line_numbers())

@app.route('/about_us')
def about_us():
    return render_template("about_us.html", active_page="about_us")


if __name__ == '__main__':
    app.run(host='0.0.0.0')
