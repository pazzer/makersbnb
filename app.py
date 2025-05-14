import os
from flask import Flask, request, render_template, redirect, session

from lib.registration_values import RegistrationValues
from lib.login_values import LoginValues
from lib.database_connection import get_flask_database_connection
from lib.user_repository import UserRepository
from lib.custom_exceptions import MakersBnbException

# Create a new Flask app
app = Flask(__name__)

# `session` admin
app.secret_key = os.urandom(24)


# == Your Routes Here ==

@app.route('/')
def empty_route():
    return redirect('/makersbnb.com')

# Registration

@app.route('/makersbnb.com')
def show_registration_form():
    return render_template('register.html', values_so_far=RegistrationValues.all_empty())


@app.route('/makersbnb.com', methods=["POST"])
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


@app.route('/makersbnb.com/registration_complete')
def registration_succeeded():
    return render_template('registration_complete.html')


# Login

@app.route('/makersbnb.com/login')
def show_login_form():
    return render_template('login.html', values_so_far=LoginValues.all_empty())

@app.route('/makersbnb.com/login', methods=['POST'])
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
            return redirect('/makersbnb.com/spaces')


# ⚠️ ⚠️ ⚠️ ⚠️ This must be removed prior to deployment ⚠️ ⚠️ ⚠️ ⚠️ #
@app.route('/makersbnb.com/dev_login')
def log_in_developer():
    db_conn = get_flask_database_connection(app)
    user_repository = UserRepository(db_conn)
    user = user_repository.find_by_email_and_password('developer@example.com', 'ev@fr£pa!ze^abcd_pw')
    assert user is not None
    session['user_id'] = user.user_id
    return redirect('/makersbnb.com/spaces')

@app.route('/makersbnb.com/logout')
def log_out():
    if 'user_id' in session:
        db_conn = get_flask_database_connection(app)
        user_repository = UserRepository(db_conn)
        user = user_repository.find_by_id(session['user_id'])
        del session['user_id']

    return redirect('/makersbnb.com/login')

# Spaces

@app.route('/makersbnb.com/spaces')
def show_spaces():
    if 'user_id' in session:
        db_conn = get_flask_database_connection(app)
        user_repository = UserRepository(db_conn)
        user = user_repository.find_by_id(session['user_id'])
        return render_template('spaces.html', user=user, dummy_space_strings=[
            '🏰 Cozy Cabin',
            '🏠 Urban Loft',
            '🛖 Beach Bungalow',
            '⛪️ Mountain Retreat',
            '🏥 Modern Studio'
        ])
    else:
        return redirect('/makersbnb.com/login')



# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
