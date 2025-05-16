class Booking:
    def __init__(self, booking_id, start_range, end_range, space_id, user_id, is_confirmed):
        self.booking_id = booking_id
        self.start_range = start_range
        self.end_range = end_range
        self.space_id = space_id
        self.user_id = user_id
        self.is_confirmed = is_confirmed

    def __eq__(self, other):
        if not isinstance(other, Booking):
            return NotImplemented
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f"Booking({self.booking_id}, {self.start_range}, {self.end_range}, {self.space_id}, {self.user_id}, {self.is_confirmed})"

    @staticmethod
    def from_rowdict(rowdict):
        return Booking(rowdict['booking_id'],
                rowdict['start_range'],
                rowdict['end_range'],
                rowdict['space_id'],
                rowdict['user_id'],
                rowdict['is_confirmed'])


    def __str__(self):
        return "stuff here"

