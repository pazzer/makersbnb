import os
from flask import Flask, request, redirect, render_template, session, flash
from lib.database_connection import get_flask_database_connection

from lib.booking import Booking
from lib.booking_repository import BookingRepository

from lib.space import Space
from lib.space_repository import SpaceRepository

# Create a new Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)

# == Your Routes Here ==

# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5001/index
@app.route('/index', methods=['GET'])
def get_index():
    return render_template('example_base_extended.html')

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
    description = request.form['description']
    price_per_night = request.form['price_per_night']
    user_id = session.get('user_id', None)

    space = Space(None, name, description, price_per_night, user_id)
    repository.add_space(space)

    flash('Your space has been added to MakersBnB!')
    return redirect(f'/myspaces/new')


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









# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
