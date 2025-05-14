import os
from flask import Flask, request, redirect, render_template
from lib.database_connection import get_flask_database_connection

from lib.booking import Booking
from lib.booking_repository import BookingRepository

# Create a new Flask app
app = Flask(__name__)

# == Your Routes Here ==

# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5001/index
@app.route('/index', methods=['GET'])
def get_index():
    return render_template('example_base_extended.html')

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
# @app.route('/spaces', methods=['GET'])
# def get_all_spaces():
#     connection = get_flask_database_connection
#     repository  = SpaceRepository(connection)
#     spaces = repository.<get_all_method_name>()
#     return render_template('spaces_all.html', spaces=spaces)

# GET / spaces/<int:space_id>
# Shows user an individual space when they click a button to view more info or book
# @app.route('/spaces/<int:space_id>', methods=['GET'])
# def get_individual_space(space_id):
#     connection = get_flask_database_connection(app)
#     repository = SpaceRepository(connection)
#     space = repository.<get_single_space>(space_id)
#     return render_template('space_individual.html', space=space)








# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
