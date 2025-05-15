from lib.login_values import LoginValues
from lib.util import to_date

class DateFilterFormValues:

    def __init__(self, start_date, end_date):
        assert start_date < end_date, 'bad arguments - start date must fall before end date'
        self.start_date = start_date
        self.end_date = end_date

    @staticmethod
    def from_post_request(request, returns_default_range_if_error=True):
        start_date = to_date(request.form['start_date'])
        end_date = to_date(request.form['end_date'])
        if not start_date < end_date:
            if returns_default_range_if_error:
                return DateFilterFormValues(to_date('01/03/2025'), to_date('01/03/2027'))
            else:
                return None
        else:
            return DateFilterFormValues(start_date, end_date)


