import os
from flask import Flask, request, render_template, redirect, session
from lib.database_connection import get_flask_database_connection

from lib.registration_values import RegistrationValues
from lib.login_values import LoginValues

from lib.custom_exceptions import MakersBnbException
from lib.user_repository import UserRepository
from lib.booking_repository import BookingRepository
from lib.space_repository import SpaceRepository

# Create a new Flask app
app = Flask(__name__)

# `session` admin
app.secret_key = os.urandom(24)

# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5001/index
@app.route('/index', methods=['GET'])
def get_index():
    return render_template('example_base_extended.html')

# The 'empty route' - redirect to register

@app.route('/')
def empty_route():
    return redirect('/register')

# ------------------------------- Registration and login  ---------------------------------------------------

@app.route('/register')
def show_registration_form():
    return render_template('register.html', values_so_far=RegistrationValues.all_empty())


@app.route('/register', methods=["POST"])
def handle_registration_request():
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
            return render_template("registration_complete.html")


@app.route('/registration_complete')
def registration_succeeded():
    return render_template('registration_complete.html')


# Login

@app.route('/login')
def show_login_form():
    return render_template('login.html', values_so_far=LoginValues.all_empty())

@app.route('/login', methods=['POST'])
def handle_login_request():
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
            session['user_id'] = user.user_id
            return redirect('/spaces')


# ⚠️ ⚠️ ⚠️ ⚠️ This must be removed prior to deployment ⚠️ ⚠️ ⚠️ ⚠️ #
@app.route('/dev_login')
def log_in_developer():
    db_conn = get_flask_database_connection(app)
    user_repository = UserRepository(db_conn)
    user = user_repository.find_by_email_and_password('developer@example.com', 'ev@fr£pa!ze^abcd_pw')
    assert user is not None
    session['user_id'] = user.user_id
    return redirect('/spaces')

@app.route('/logout')
def log_out():
    if 'user_id' in session:
        db_conn = get_flask_database_connection(app)
        user_repository = UserRepository(db_conn)
        user = user_repository.find_by_id(session['user_id'])
        del session['user_id']

    return redirect('/login')

# Spaces

# @app.route('/spaces')
# def show_spaces():
#     if 'user_id' in session:
#         db_conn = get_flask_database_connection(app)
#         user_repository = UserRepository(db_conn)
#         user = user_repository.find_by_id(session['user_id'])
#         return render_template('spaces.html', user=user, dummy_space_strings=[
#             '🏰 Cozy Cabin',
#             '🏠 Urban Loft',
#             '🛖 Beach Bungalow',
#             '⛪️ Mountain Retreat',
#             '🏥 Modern Studio'
#         ])
#     else:
#         return redirect('/login')




# ------------------------ manage spaces page ---------------------------------------------

@app.route('/myspaces/manage', methods=['GET'])
def space_manager():
    user_id = session.get('user_id', None)
    if user_id is not None:
        connection = get_flask_database_connection(app)
        repository = SpaceRepository(connection)
        spaces = repository.find_for_user(user_id)
        return render_template('space_manager.html', spaces=spaces)
    else:
        return redirect(f'/login')

# ------------------------ bookings routes ------------------------------------------------------

# GET /myspaces/bookings/<space_id>
# Returns confirmed bookings for a space
@app.route('/myspaces/bookings/<int:space_id>', methods=['GET'])
def get_bookings(space_id):
    connection = get_flask_database_connection(app)
    repository = BookingRepository(connection)
    bookings = repository.view_bookings(space_id)
    return render_template('myspaces_bookings.html', bookings=bookings)

# GET /myspaces/requests/<space_id>
# Returns requests to book for a space
@app.route('/myspaces/requests/<int:space_id>', methods=['GET'])
def get_requests(space_id):
    connection = get_flask_database_connection(app)
    repository = BookingRepository(connection)
    requests = repository.view_requests(space_id)
    return render_template('myspaces_requests.html', requests=requests)

#  POST (DELETE) myspaces/requests/<space_id>/<booking_id>/reject
# Deletes a request when it is rejected
@app.route('/myspaces/requests/<int:space_id>/<int:booking_id>/reject', methods=['POST'])
def delete_request(booking_id, space_id):
    connection = get_flask_database_connection(app)
    repository = BookingRepository(connection)
    repository.reject_request(booking_id)
    return redirect(f'/myspaces/requests/{space_id}')

# POST (PUT) myspaces/requests/<space_id>/<booking_id>/accept
# Accepts a booking request and changes is_confirmed to true
@app.route('/myspaces/requests/<int:space_id>/<int:booking_id>/accept', methods=['POST'])
def accept_request(booking_id, space_id):
    connection = get_flask_database_connection(app)
    repository = BookingRepository(connection)
    repository.approve_request(booking_id)
    return redirect(f'/myspaces/requests/{space_id}')

# -------------------------------------------- Spaces routes ---------------------------------------------------

# GET / spaces
# Shows user all spaces listed on our website as soon as they log in
@app.route('/spaces', methods=['GET'])
def get_all_spaces():
    session['user_id'] = 1
    connection = get_flask_database_connection(app)
    repository  = SpaceRepository(connection)
    spaces = repository.list_spaces()
    return render_template('spaces_all.html', spaces=spaces)

# GET / spaces/<int:space_id>
# Shows user an individual space when they click a button to view more info or book
@app.route('/spaces/<int:space_id>', methods=['GET'])
def get_individual_space(space_id):
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)
    space = repository.find(space_id)
    return render_template('space_individual.html', space=space)


# ------------------------------ manage spaces page ---------------------------------------------
@app.route('/myspaces/manage', methods=['GET'])
def space_manager():
    user_id = session.get('user_id', None)
    if user_id is not None:
        connection = get_flask_database_connection(app)
        repository = SpaceRepository(connection)
        spaces = repository.find_for_user(user_id)
        return render_template('space_manager.html', spaces=spaces)
    else:
        return redirect(f'/login')

# ---------------------------------------------- bookings routes ------------------------------------------------------------
# GET /myspaces/bookings/<space_id>
# Returns confirmed bookings for a space
@app.route('/myspaces/bookings/<int:space_id>', methods=['GET'])
def get_bookings(space_id):
    connection = get_flask_database_connection(app)
    repository = BookingRepository(connection)
    bookings = repository.view_bookings(space_id)
    return render_template('myspaces_bookings.html', bookings=bookings)

# GET /myspaces/requests/<space_id>
# Returns requests to book for a space
@app.route('/myspaces/requests/<int:space_id>', methods=['GET'])
def get_requests(space_id):
    connection = get_flask_database_connection(app)
    repository = BookingRepository(connection)
    requests = repository.view_requests(space_id)
    return render_template('myspaces_requests.html', requests=requests)

#  POST (DELETE) myspaces/requests/<space_id>/<booking_id>/reject
# Deletes a request when it is rejected
@app.route('/myspaces/requests/<int:space_id>/<int:booking_id>/reject', methods=['POST'])
def delete_request(booking_id, space_id):
    connection = get_flask_database_connection(app)
    repository = BookingRepository(connection)
    repository.reject_request(booking_id)
    return redirect(f'/myspaces/requests/{space_id}')

# POST (PUT) myspaces/requests/<space_id>/<booking_id>/accept
# Accepts a booking request and changes is_confirmed to true
@app.route('/myspaces/requests/<int:space_id>/<int:booking_id>/accept', methods=['POST'])
def accept_request(booking_id, space_id):
    connection = get_flask_database_connection(app)
    repository = BookingRepository(connection)
    repository.approve_request(booking_id)
    return redirect(f'/myspaces/requests/{space_id}')

# -------------------------------------------- Spaces routes ---------------------------------------------------

# GET / spaces
# Shows user all spaces listed on our website as soon as they log in
@app.route('/spaces', methods=['GET'])
def get_all_spaces():
    session['user_id'] = 1
    connection = get_flask_database_connection(app)
    repository  = SpaceRepository(connection)
    spaces = repository.list_spaces()
    return render_template('spaces_all.html', spaces=spaces)

# GET / spaces/<int:space_id>
# Shows user an individual space when they click a button to view more info or book
@app.route('/spaces/<int:space_id>', methods=['GET'])
def get_individual_space(space_id):
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)
    space = repository.find(space_id)
    return render_template('space_individual.html', space=space)








# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
