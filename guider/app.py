from flask import request, jsonify, flash, get_flashed_messages
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
    """
    Renders the template for the homepage
    """
    return render_template('home.html', active_page='home')


@app.route('/cities', methods=['GET', 'POST'])
def cities():
    """
    Renders the cities page/form
    """
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
    trigger = 'True' if not trigger else 'load_trigger'
    # if form was submitted, use redirect
    if city_form.validate_on_submit():
        # extract route from form, allow route to be opened in new page
        map_route = city_form.handle_route()
        app.log_request(map_route)
        target = '_blank'
        # redirect
        return redirect(url_for('cities', route=map_route, target=target, trigger=trigger))
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
    """
    Python code to compute the best route
    """
    print('Handling route')
    # sleep to have a chance for the spinning wheel to shine
    time.sleep(5)
    # compute the route
    dir_build = DirectionBuilder(app.maps_api_key, app.last_route)
    # return the best route
    return jsonify(dir_build.directions)


@app.route('/the_idea')
def the_idea():
    """
    Renders the template describing the startup
    """
    return render_template('the_idea.html', active_page='the_idea')


@app.route('/about_us/render_marie', methods=['GET', 'POST'])
def marie_form():
    """
    Renders the page to enter MARIE simulator code
    """

    mform = forms.MarieSimCode()

    if mform.validate_on_submit():
        # if code is submitted, parse the code
        parser = Parser(mform.code.data)
        # store the submitted code/parser object
        app.store_parsed_marie(parser)
        # render the parsed code nicely
        return redirect(url_for("display_marie"))
    return render_template("msim_submit.html", form=mform, active_page='about_us')


@app.route("/about_us/rendered_marie")
def display_marie():
    """
    Renders submitted MARIE simulator code
    """
    return render_template("msim_rendered.html",
                           active_page='about_us',
                           rendered_code=app.marie_parser.render_html(),
                           rendered_lines=app.marie_parser.html_line_numbers())

@app.route('/about_us')
def about_us():
    """
    Renders about us page
    """
    return render_template("about_us.html", active_page="about_us")


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    """
    Renders sign up page, handles submitting new sign up information
    """
    signup_form = forms.SignUpForm()

    if request.method == 'GET':
        # if a get request, make sure the form renders as empty
        signup_form.set_empty_string()

    if signup_form.validate_on_submit():
        # transform and insert the data
        signup_form.transform()
        signup_form.insert()
        return redirect(url_for('sign_up'))
    if request.method == 'POST':
        print(signup_form)
        e = [(flash(li), print(li)) for lst in signup_form._fields.values() for li in lst.errors]
        [print(e2) for e2 in get_flashed_messages()]


    return render_template('sign_up.html', form=signup_form)


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    signin_form = forms.SignInForm()

    if request.method == 'GET':
        signin_form.set_empty_string()
    print(signin_form)
    if signin_form.validate_on_submit():
        return redirect(url_for('cities'))

    return render_template('signin.html', form=signin_form)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
