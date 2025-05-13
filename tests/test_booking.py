from lib.booking import Booking
from lib.booking_repository import BookingRepository
from lib.util import str_to_date, date_to_str

import datetime

# Methods: view_bookings, view_requests, create_request, reject_request, approve_request

# Test view_bookings returns all confirmed viewings
def test_view_bookings(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = BookingRepository(db_connection)

    bookings = repository.view_bookings(1)

    assert bookings == []

#  Test view_bookings returns all confirmed viewings
def test_view_requests(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = BookingRepository(db_connection)

    bookings = repository.view_requests(2)

    assert bookings[0] == Booking(2, str_to_date('2025/06/06'), str_to_date('2025/06/09'), 2, 3, False)

#  Test create request, adds a new request to the bookings table, and is_confirmed is false
def test_create_request(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = BookingRepository(db_connection)

    repository.create_request(Booking(6, str_to_date('2025/06/06'), str_to_date('2025/06/09'), 5, 4, False))

    assert repository.view_requests(5) == [
        Booking(5, str_to_date('2025/08/02'), str_to_date('2025/08/06'), 5, 1, False),
        Booking(6, str_to_date('2025/06/06'), str_to_date('2025/06/09'), 5, 4, False)
    ]

# Test reject a request by deleting the column
def test_reject_request(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = BookingRepository(db_connection)

    repository.reject_request(5)

    assert repository.view_requests(5) == []

# Test approve a request by changing is_confirmed from false to true
def test_approve_request(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = BookingRepository(db_connection)

    repository.approve_request(5)

    assert repository.view_bookings(5) == [Booking(5, str_to_date('2025/08/02'), str_to_date('2025/08/06'), 5, 1, True)]


