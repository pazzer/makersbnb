from lib.booking import Booking

class BookingRepository:
    def __init__(self, connection):
        self.connection = connection

    # See all confirmed bookings for a space
    def view_bookings(self, space_id):
        rows = self.connection.execute('SELECT ALL WHERE space_id = %s AND is_confirmed = TRUE', [space_id])
        spaces = []
        for row in rows:
            item = Booking(row['booking_id'], row['start_range'], row['end_range'], row['space_id'], row['user_id'], row['is_confirmed'])
            spaces.append(item)
        return spaces

    # See all requests (unconfirmed bookings) for a space
    def view_requests(self, space_id):
        rows = self.connection.execute('SELECT ALL WHERE space_id = %s AND is_confirmed = FALSE', [space_id])
        spaces = []
        for row in rows:
            item = Booking(row['booking_id'], row['start_range'], row['end_range'], row['space_id'], row['user_id'], row['is_confirmed'])
            spaces.append(item)
        return spaces
    
    # Create a new booking request
    def create_requests(self, booking):
        rows = self.connection.execute('INSERT INTO bookings (start_range, end_range, space_id, user_id, is_confirmed) VALUES(%s, %s, %s, %s, FALSE) RETURNING booking_id', [booking.start_range, booking.end_range, booking.space_id, booking.user_id])
        row = rows[0]
        booking.booking_id = row['booking_id']
        return booking.booking_id # returning booking id here as potential to provide customer with booking number after they submit booking
    
    #  Delete a booking request using booking_id?
    def reject_request(self, booking_id):
        self.connection.execute('DELETE FROM bookings WHERE booking_id = %s', [booking_id])
        return None


    # Approve a booking request aka is_confirmed TRUE to FALSE| basic approve a request which bares no effect on on other requests for the same space on overlapping days
    def approve_request(self, booking_id):
        rows = self.connection.execute('UPDATE bookings SET is_confirmed = FALSE WHERE booking_id = %s', [booking_id])