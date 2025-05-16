import os

import flask
from flask import Flask, request, render_template, redirect, flash
from flask_login import login_required, current_user

from lib.BookingRequestFormValues import BookingRequestFormValues
from lib.database_connection import get_flask_database_connection

from lib.registration_values import RegistrationValues
from lib.login_values import LoginValues
from lib.date_filter_form_values import DateFilterFormValues
from lib.custom_exceptions import MakersBnbException
from lib.user_repository import UserRepository
from lib.booking_repository import BookingRepository

from lib.booking import Booking
from lib.space_repository import SpaceRepository
from lib.space import Space
from lib.util import to_date, format_date_range

import flask_login

login_manager = flask_login.LoginManager()
login_manager.login_view = 'login'
app = Flask(__name__)
app.config['TESTING'] = True
app.secret_key = os.urandom(24)
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(id_):
    db_conn = get_flask_database_connection(app)
    user_repository = UserRepository(db_conn)
    user = user_repository.find_by_id(id_)
    return user if user is not None else None

@app.route('/index', methods=['GET'])
def get_index():
    return render_template('example_base_extended.html')

# The 'empty route' - redirect to register

@app.route('/')
def empty_route():
    return redirect('/register')


# ------------------------------- Registration and login  ---------------------------------------------------

@app.route('/register', methods=['POST', 'GET'])
def handle_registration_request():

    if request.method == 'POST':
        registration_values = RegistrationValues.from_post_request(request)

        db_conn = get_flask_database_connection(app)
        user_repository = UserRepository(db_conn)

        if registration_values.has_errors():
            first_error = registration_values.first_error()
            return render_template(
                'register.html',
                errors=first_error,
                values_so_far=registration_values)
        else:
            try:
                user_repository.create_user(registration_values.email, registration_values.password_1)
            except MakersBnbException as err:
                return render_template(
                    "register.html",
                    errors= str(err),
                    values_so_far=registration_values)
            else:
                return redirect('/registration_complete')
                # return render_template("registration_complete.html")
    else:
        return render_template('register.html',
                               values_so_far=RegistrationValues.all_empty())


@app.route('/registration_complete')
def registration_succeeded():
    return render_template('registration_complete.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user is not None:
            flask_login.logout_user()
        return render_template('login.html',
                               values_so_far=LoginValues.all_empty())
    else:

        login_values = LoginValues.from_post_request(request)

        db_conn = get_flask_database_connection(app)
        user_repository = UserRepository(db_conn)

        if login_values.has_errors():
            return render_template(
                'login.html',
                errors="⚠️ " + login_values.first_error(),
                values_so_far=login_values)
        else:
            user = user_repository.find_by_email_and_password(login_values.email, login_values.password)
            if user is None:
                return render_template(
                    'login.html',
                    errors="⛔ email and/or password not recognised. Try Again.",
                    values_so_far=login_values)
            else:
                flask_login.login_user(user)
                return flask.redirect(flask.url_for('display_spaces'))

@app.route('/logout')
@flask_login.login_required
def log_out():
    flask_login.logout_user()
    return redirect('/login')


@app.route('/user_account')
@flask_login.login_required
def user_account():
    return render_template('user_account.html')


# ⚠️ ⚠️ ⚠️ ⚠️ Must NOT ship ⚠️ ⚠️ ⚠️ ⚠️ #
@app.route('/dev_login')
# Remove line below to allow dev login
# @flask_login.login_required
def log_in_developer():
    db_conn = get_flask_database_connection(app)
    user_repository = UserRepository(db_conn)
    user = user_repository.find_by_email_and_password('developer@example.com', 'ev@fr£pa!ze^abcd_pw')
    flask_login.login_user(user)
    return redirect(flask.url_for('display_spaces'))




# ------------------------ bookings routes ------------------------------------------------------

# GET /myspaces/bookings/<space_id>
# Returns confirmed bookings for a space
@app.route('/myspaces/bookings/<int:space_id>', methods=['GET'])
@flask_login.login_required
def get_bookings(space_id):
    connection = get_flask_database_connection(app)
    repository = BookingRepository(connection)
    bookings = repository.view_bookings(space_id)
    return render_template('myspaces_bookings.html', bookings=bookings)

# GET /myspaces/requests/<space_id>
# Returns requests to book for a space
@app.route('/myspaces/requests/<int:space_id>', methods=['GET'])
@flask_login.login_required
def get_requests(space_id):
    connection = get_flask_database_connection(app)
    repository = BookingRepository(connection)
    space_repository = SpaceRepository(connection)
    space = space_repository.find(space_id)
    requests = repository.view_requests(space_id)
    return render_template('myspaces_requests.html', requests=requests, space=space)

#  POST (DELETE) myspaces/requests/<space_id>/<booking_id>/reject
# Deletes a request when it is rejected
@app.route('/myspaces/requests/<int:space_id>/<int:booking_id>/reject', methods=['POST'])
@flask_login.login_required
def delete_request(booking_id, space_id):
    connection = get_flask_database_connection(app)
    repository = BookingRepository(connection)
    repository.reject_request(booking_id)
    return redirect(f'/myspaces/requests/{space_id}')

# POST (PUT) myspaces/requests/<space_id>/<booking_id>/accept
# Accepts a booking request and changes is_confirmed to true
@app.route('/myspaces/requests/<int:space_id>/<int:booking_id>/accept', methods=['POST'])
@flask_login.login_required
def accept_request(booking_id, space_id):
    connection = get_flask_database_connection(app)
    repository = BookingRepository(connection)
    repository.approve_request(booking_id)
    return redirect(f'/myspaces/requests/{space_id}')

# -------️------------------------------------- Spaces routes ---------------------------------------------------

# GET / new space form page
# Displays the form to create a new space
@app.route('/myspaces/new', methods=['GET'])
@flask_login.login_required
def new_space_form():
    return render_template('myspaces_new.html')

# POST / myspaces/new
# CReates new space
@app.route('/myspaces/new', methods=['POST'])
@flask_login.login_required
def create_space():
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)

    name = request.form['name']
    description = request.form['description']
    price_per_night = request.form['price_per_night']
    user_id = flask_login.current_user.user_id

    space = Space(None, name, description, price_per_night, user_id)
    repository.add_space(space)

    flash('Your space has been added to MakersBnB!')
    return redirect(f'/myspaces/new')



# GET spaces/filtered
# Shows the user suitable spaces depending on their date range

@app.route('/spaces', methods=['GET', 'POST'])
@flask_login.login_required
def display_spaces():
    connection = get_flask_database_connection(app)
    if request.method == 'POST':
        date_field_values = DateFilterFormValues.from_post_request(request)
    else:
        date_field_values = DateFilterFormValues.default_range()

    space_repository = SpaceRepository(connection)
    spaces, owners = space_repository.spaces_and_owners_for_dates(*date_field_values.values())

    return render_template('spaces.html',
                           spaces_and_owners=zip(spaces, owners),
                           date_range=date_field_values,
                           result_count=len(spaces))


# GET / spaces/<int:space_id>
# Shows user an individual space when they click a button to view more info or book
@app.route('/spaces/<int:space_id>/<start_date>+<end_date>', methods=['GET'])
@flask_login.login_required
def display_space(space_id, start_date, end_date):
    connection = get_flask_database_connection(app)
    space_repository = SpaceRepository(connection)
    space = space_repository.find(space_id)
    user_repository = UserRepository(connection)
    owner = user_repository.get_owner_of_space(space)
    start = to_date(start_date)
    end = to_date(end_date)
    formatted_range = format_date_range(start, end)
    return render_template('space_individual.html',
                               space=space,
                               owner=owner,
                               start_date=start,
                               end_date=end,
                               formatted_dates=formatted_range)



@app.route('/spaces/book', methods=['POST'])
@flask_login.login_required
def submit_booking_request():
    connection = get_flask_database_connection(app)
    repository = BookingRepository(connection)
    booking_params = BookingRequestFormValues.from_post_request(request)
    booking = Booking(None,
            start_range=booking_params.start_date,
            end_range=booking_params.end_date,
            space_id=booking_params.space_id,
            user_id=current_user.get_id(),
            is_confirmed=False)

    _ = repository.create_request(booking)
    # TODO: return something here!




# ------------------------------ manage spaces page ---------------------------------------------
@app.route('/myspaces/manage', methods=['GET'])
@flask_login.login_required
def space_manager():
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)
    spaces = repository.find_for_user(current_user.user_id)
    return render_template('space_manager.html', spaces=spaces)


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
