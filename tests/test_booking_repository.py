# __created_by__ == Paul Patterson

from lib.booking_repository import BookingRepository
from lib.util import to_date


def test_confirmed_bookings_is_true_when_req_start_date_overlaps_confirmed_booking(db_connection):
    # Requested start date overlaps Alice's confirmed October holiday
    booking_repository = BookingRepository(db_connection)
    start, end = to_date('2025/10/08'), to_date('2025/10/14')
    assert booking_repository.has_confirmed_booking(6, start, end)


def test_confirmed_bookings_is_true_when_req_end_date_overlaps_a_confirmed_booking(db_connection):
    # Requested end date overlaps the first day of Bob's confirmed November holiday
    booking_repository = BookingRepository(db_connection)
    start, end = to_date('2025/11/13'), to_date('2025/11/17')
    assert booking_repository.has_confirmed_booking(6, start, end)


def test_confirmed_bookings_is_false_when_req_end_date_is_day_before_confirmed_start_date(db_connection):
    # Requested end date is day before Bob's confirmed November holiday
    booking_repository = BookingRepository(db_connection)
    start, end = to_date('2025/11/13'), to_date('2025/11/16')
    assert not booking_repository.has_confirmed_booking(6, start, end)


def test_confirmed_bookings_is_false_when_req_dates_fit_snugly_between_confirmed_booking(db_connection):
    # Requested dates fall exactly between Dave's first December holiday and his second, so no collision.
    booking_repository = BookingRepository(db_connection)
    start, end = to_date('2025/12/26'), to_date('2025/12/28')
    assert not booking_repository.has_confirmed_booking(6, start, end)

    # Sanity check: adding one day to end of holiday overlaps Dave's second December holiday, so collision
    start, end = to_date('2025/12/26'), to_date('2025/12/29')
    assert booking_repository.has_confirmed_booking(6, start, end)


def test_confirmed_bookings_correctly_ignores_unconfirmed_requests(db_connection):
    # These dates overlap three booking requests, but because they are all unconfirmed has_confirmed will ignore them
    # and return False.
    booking_repository = BookingRepository(db_connection)
    start, end = to_date('2025/12/09'), to_date('2025/12/13')
    assert not booking_repository.has_confirmed_booking(6, start, end)
