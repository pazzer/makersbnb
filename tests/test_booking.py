from lib.booking import Booking
from lib.booking_repository import BookingRepository
from lib.util import to_date, date_to_str

import datetime

# Methods: view_bookings, view_requests, create_request, reject_request, approve_request

ALICE = 1
BOB = 2
CAROL = 3
DAVE = 4
EVE = 5

COZY_CABIN = 1
URBAN_LOFT = 2
BEACH_BUNGALOW = 3
MOUNTAIN_RETREAT = 4
MODERN_STUDIO = 5



# Test view_bookings returns all confirmed viewings
def test_view_bookings(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = BookingRepository(db_connection)

    bookings = repository.view_bookings(COZY_CABIN)

    assert bookings == []

#  Test view_bookings returns all confirmed viewings
def test_view_requests(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = BookingRepository(db_connection)

    bookings = repository.view_requests(URBAN_LOFT)

    assert bookings[0] == Booking(2, to_date('2025/06/06'), to_date('2025/06/09'), URBAN_LOFT, CAROL, False)

#  Test create request, adds a new request to the bookings table, and is_confirmed is false
def test_create_request(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = BookingRepository(db_connection)

    modern_studio_requests = repository.view_requests(MODERN_STUDIO)

    # Dave makes a request to book Modern Studio owned by Eve
    repository.create_request(Booking(None, to_date('2025/06/06'), to_date('2025/06/09'), MODERN_STUDIO, DAVE, False))

    # Modern Studio, owned by Eve
    assert repository.view_requests(MODERN_STUDIO) == [

        # Booking request just made by Dave
        Booking(10, to_date('2025/06/06'), to_date('2025/06/09'), MODERN_STUDIO, DAVE, False),

        # Booking request just made by Carol
        Booking(9, to_date('2025/07/02'), to_date('2025/07/06'), MODERN_STUDIO, CAROL, False),

        # Booking request made by Alice
        Booking(5, to_date('2025/08/02'), to_date('2025/08/06'), MODERN_STUDIO, ALICE, False),


    ]

# Test reject a request by deleting the column
def test_reject_request(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = BookingRepository(db_connection)

    repository.reject_request(4)

    assert repository.view_requests(MOUNTAIN_RETREAT) == []

# Test approve a request by changing is_confirmed from false to true
def test_approve_request(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = BookingRepository(db_connection)

    repository.approve_request(5)

    assert repository.view_bookings(MODERN_STUDIO) == [
        Booking(7, to_date('2025/06/17'), to_date('2025/06/22'), MODERN_STUDIO, BOB, True),
        Booking(8, to_date('2025/07/02'), to_date('2025/07/06'), MODERN_STUDIO, DAVE, True),
        Booking(5, to_date('2025/08/02'), to_date('2025/08/06'), MODERN_STUDIO, ALICE, True),
        Booking(6, to_date('2025/08/04'), to_date('2025/08/11'), MODERN_STUDIO, BOB, True)
        ]


