# __created_by__ == Paul Patterson

from lib.util import to_date

class BookingRequestFormValues:

    def __init__(self, start_date, end_date, space_id, customer_id):
        self.start_date = start_date
        self.end_date = end_date
        self.space_id = space_id
        self.customer_id = customer_id

    @staticmethod
    def from_post_request(request):
        start_date = to_date(request.form['start_date'])
        end_date = to_date(request.form['end_date'])
        space_id = int(request.form['space_id'])
        customer_id = int(request.form['customer_id'])
        return BookingRequestFormValues(start_date, end_date, space_id, customer_id)

    def values(self):
        return [self.start_date, self.end_date, self.space_id, self.customer_id]
