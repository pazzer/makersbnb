import os
from flask import Flask, request, render_template, redirect, session, flash
from lib.database_connection import get_flask_database_connection

from lib.registration_values import RegistrationValues
from lib.login_values import LoginValues
from lib.date_filter_form_values import DateFilterFormValues
from lib.custom_exceptions import MakersBnbException
from lib.user_repository import UserRepository
from lib.booking_repository import BookingRepository

from lib.space import Space
from lib.space_repository import SpaceRepository
from lib.space import Space

from lib.available_range_repo import AvailableRangeRepo


import mailtrap as mt
from static.token import token

# Create a new Flask app
app = Flask(__name__)

# `session` admin
app.secret_key = os.urandom(24)

def get_session_user(db_conn):
    user_id = session['user_id']
    user_repository = UserRepository(db_conn)
    return user_repository.find_by_id(user_id)

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
    return render_template('register.html', values_so_far=RegistrationValues.all_empty(), no_active_session=True)


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

            #email stuff
            user_email = registration_values.email

            #

            mail = mt.Mail(
            sender=mt.Address(email="hello@demomailtrap.co", name="Mailtrap Test"),
            to=[mt.Address(email="eveiaim98@outlook.com")],
            subject="Thank you for registering!",
            text=f"{user_email} has just been registered to makersbnb",
            category="Integration Test",
            )

            client = mt.MailtrapClient(token = token())
            response = client.send(mail)

            print(response)
            #



            return render_template("registration_complete.html")


@app.route('/registration_complete')
def registration_succeeded():
    return render_template('registration_complete.html')


# Login

@app.route('/login')
def show_login_form():
    if 'user_id' in session: del session['user_id']
    return render_template('login.html',
                           values_so_far=LoginValues.all_empty(),
                           no_active_session=True)

@app.route('/login', methods=['POST'])
def handle_login_request():
    login_values = LoginValues.from_post_request(request)

    db_conn = get_flask_database_connection(app)
    user_repository = UserRepository(db_conn)

    if login_values.has_errors():
        return render_template(
            'login.html',
            errors="⚠️ " + login_values.first_error(),
            values_so_far=login_values,
            no_active_session=True)
    else:
        user = user_repository.find_by_email_and_password(login_values.email, login_values.password)
        if user is None:
            return render_template(
                'login.html',
                errors="⛔ email and/or password not recognised. Try Again.",
                values_so_far=login_values,
                no_active_session=True)
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
    space_repository = SpaceRepository(connection)
    space = space_repository.find(space_id)
    requests = repository.view_requests(space_id)
    return render_template('myspaces_requests.html', requests=requests, space=space)

#  POST (DELETE) myspaces/requests/<space_id>/<booking_id>/reject
# Deletes a request when it is rejected
@app.route('/myspaces/requests/<int:space_id>/<int:booking_id>/reject', methods=['POST'])
def delete_request(booking_id, space_id):
    connection = get_flask_database_connection(app)
    repository = BookingRepository(connection)
    

    #email stuff
    user_repo = UserRepository(connection)
    booking = repository.view_by_id(booking_id)
    user_id = booking.user_id
    user = user_repo.find_by_id(user_id)
    user_email = user.email_address

    space_repo = SpaceRepository(connection)
    space = space_repo.find(space_id)
    space_name = space.name

    #

    mail = mt.Mail(
    sender=mt.Address(email="hello@demomailtrap.co", name="Mailtrap Test"),
    to=[mt.Address(email="eveiaim98@outlook.com")],
    subject="Booking Rejection of makersbnb!",
    text=f"{user_id} your booking for {space_name} has been denied by admin",
    category="Integration Test",
    )

    client = mt.MailtrapClient(token = token())
    response = client.send(mail)

    print(response)
    #

    #normal stuff
    repository.reject_request(booking_id)
    return redirect(f'/myspaces/requests/{space_id}')


# POST (PUT) myspaces/requests/<space_id>/<booking_id>/accept
# Accepts a booking request and changes is_confirmed to true
@app.route('/myspaces/requests/<int:space_id>/<int:booking_id>/accept', methods=['POST'])
def accept_request(booking_id, space_id):
    connection = get_flask_database_connection(app)
    repository = BookingRepository(connection)
    repository.approve_request(booking_id)

    #email stuff
    user_repo = UserRepository(connection)
    booking = repository.view_by_id(booking_id)
    user_id = booking.user_id
    user = user_repo.find_by_id(user_id)
    user_email = user.email_address

    space_repo = SpaceRepository(connection)
    space = space_repo.find(space_id)
    space_name = space.name

    #

    mail = mt.Mail(
    sender=mt.Address(email="hello@demomailtrap.co", name="Mailtrap Test"),
    to=[mt.Address(email="eveiaim98@outlook.com")],
    subject="Booking Confirmation of makersbnb!",
    text=f"{user_id} your booking for {space_name} has been confirmed by admin",
    category="Integration Test",
    )

    client = mt.MailtrapClient(token = token()) #just copy paste the token as a string here
    response = client.send(mail)

    print(response)
    #

    #normal stuff
    return redirect(f'/myspaces/requests/{space_id}')

# -------------------------------------------- Spaces routes ---------------------------------------------------

# GET / new space form page
# Displays the form to create a new space
@app.route('/myspaces/new', methods=['GET'])
def new_space_form():
    return render_template('myspaces_new.html')

# POST / myspaces/new
# CReates new space
@app.route('/myspaces/new', methods=['POST'])
def create_space():
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)

    name = request.form['name']
    short_description = request.form['short_description']
    long_description = request.form['long_description']
    area = request.form['area']
    country = request.form['country']
    price_per_night = request.form['price_per_night']
    user_id = session.get('user_id', None)

    space = Space(None, name, short_description, long_description, area, country, price_per_night, user_id)
    repository.add_space(space)

    flash('Your space has been added to MakersBnB!')
    return redirect(f'/myspaces/new')


# GET / spaces
# Shows user all spaces listed on our website as soon as they log in
@app.route('/spaces', methods=['GET'])
def get_all_spaces():
    connection = get_flask_database_connection(app)
    user = get_session_user(connection)
    space_repository  = SpaceRepository(connection)
    user_repository = UserRepository(connection)
    spaces = space_repository.list_spaces()
    owners = [user_repository.get_owner_of_space(space) for space in spaces]
    return render_template('spaces_all.html', spaces_and_owners=zip(spaces, owners), logged_in=user.name)

# GET spaces/filtered
# Shows the user suitable spaces depending on their date range
@app.route('/spaces/filtered', methods=['POST'])
def get_filtered_spaces():
    connection = get_flask_database_connection(app)
    user = get_session_user(connection)
    space_repository = SpaceRepository(connection)
    user_repository = UserRepository(connection)
    filter_range = DateFilterFormValues.from_post_request(request)
    spaces = space_repository.list_spaces_by_date_range(filter_range.start_date, filter_range.end_date)
    owners = [user_repository.find_by_id(space.user_id) for space in spaces]
    return render_template('spaces_all.html', spaces_and_owners=zip(spaces, owners), logger_in=user.name)


# GET / spaces/<int:space_id>
# Shows user an individual space when they click a button to view more info or book
@app.route('/spaces/<int:space_id>', methods=['GET'])
def get_individual_space(space_id):
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)
    space = repository.find(space_id)
    user_repository = UserRepository(connection)
    user = user_repository.get_owner_of_space(space)
    return render_template('space_individual.html', space=space, owner=user)




# POST / spaces/<int:space_id>/book
# Creating a booking request
# @app.route('/spaces/<int:space_id>/book', methods=['POST'])
# def post_request(space_id):
    
#     connection = get_flask_database_connection(app)
#     repository = BookingRepository(connection)

#     start_range = request.form['start_range']
#     end_range = request.form['end_range']
#     user_id = session.get('user_id', None)

#     booking = BookingRepository(None, start_range, end_range, space_id, user_id, False)

#     repository.create_request(booking)

#     return redirect(f'/spaces/<int:space_id>/book/sent')

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

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
