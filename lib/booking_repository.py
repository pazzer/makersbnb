from lib.booking import Booking
from lib.custom_exceptions import UnrecognisedIdError

class BookingRepository:
    def __init__(self, connection):
        self.connection = connection

    # See all confirmed bookings for a space
    def view_bookings(self, space_id):
        rows = self.connection.execute('SELECT * FROM bookings WHERE space_id = %s AND is_confirmed = TRUE ORDER BY start_range', [space_id])
        spaces = []
        for row in rows:
            item = Booking(row['booking_id'], row['start_range'], row['end_range'], row['space_id'], row['user_id'], row['is_confirmed'])
            spaces.append(item)
        return spaces

    #email stuff
    def view_by_id(self, booking_id):
        rows = self.connection.execute('SELECT * FROM bookings WHERE booking_id = %s', [booking_id])
        row = rows[0]
        item = Booking(row['booking_id'], row['start_range'], row['end_range'], row['space_id'], row['user_id'], row['is_confirmed'])
        return item



    # See all requests (unconfirmed bookings) for a space
    def find_by_id(self, id_):
        """Returns the `User` associated with `id_`. If no match is found an AssertionError
        is thrown."""
        rows = self.connection.execute("SELECT * FROM bookings WHERE booking_id = %s", [id_])
        if len(rows) != 1:
            raise UnrecognisedIdError(f"id '{id_}' not recognized.")
        else:
            return Booking.from_rowdict(rows[0])


    def view_requests(self, space_id):
        '''See all requests (unconfirmed bookings) for a given space_id'''
        rows = self.connection.execute('SELECT * FROM bookings WHERE space_id = %s AND is_confirmed = FALSE ORDER BY start_range', [space_id])
        spaces = []
        for row in rows:
            item = Booking(row['booking_id'], row['start_range'], row['end_range'], row['space_id'], row['user_id'], row['is_confirmed'])
            spaces.append(item)
        return spaces
    
    # Create a new booking request
    def create_request(self, booking):
        rows = self.connection.execute('INSERT INTO bookings (start_range, end_range, space_id, user_id, is_confirmed) VALUES(%s, %s, %s, %s, FALSE) RETURNING booking_id', [booking.start_range, booking.end_range, booking.space_id, booking.user_id])
        row = rows[0]
        booking.booking_id = row['booking_id']
        return booking.booking_id # returning booking id here as potential to provide customer with booking number after they submit booking
    
    #  Delete a booking request using booking_id?
    def reject_request(self, booking_id):
        self.connection.execute('DELETE FROM bookings WHERE booking_id = %s', [booking_id])
        return None


    # Approve a booking request aka is_confirmed FALSE to TRUE| basic approve request which bares no effect on on other requests for the same space on overlapping days
    def approve_request(self, booking_id):
        rows = self.connection.execute('UPDATE bookings SET is_confirmed = TRUE WHERE booking_id = %s', [booking_id])



    def has_confirmed_booking(self, space_id, start_date, end_date):
        '''Returns True if the provided space already has a confirmed booking that overlaps the provided range'''
        confirmed_bookings = self.connection.execute('SELECT booking_id FROM bookings'
                                                     ' WHERE space_id = %s '
                                                     'AND '
                                                     '(%s BETWEEN start_range and end_range '
                                                     'OR '
                                                     '%s BETWEEN start_range and end_range) '
                                                     'AND'
                                                     ' is_confirmed IS TRUE', [space_id, start_date, end_date] )
        return len(confirmed_bookings) > 0
