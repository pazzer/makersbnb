import os
from flask import Flask, request, render_template, redirect

from lib.RegistrationValues import RegistrationValues
from lib.database_connection import get_flask_database_connection
from lib.user_repository import UserRepository
from lib.custom_exceptions import MakersBnbException

# Create a new Flask app
app = Flask(__name__)

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
        return render_template('register.html', errors=first_error, values_so_far=registration_values)
    else:
        try:
            user_repository.register_new_user(registration_values.email, registration_values.password_1)
        except MakersBnbException as err:
            return render_template("register.html", errors= str(err), values_so_far=registration_values)
        else:
            return render_template("registration_complete.html")


@app.route('/makersbnb.com/registration_complete')
def registration_succeeded():
    return render_template('registration_complete.html')


# Login

@app.route('/makersbnb.com/login')
def login():
    return render_template('login.html')





# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
