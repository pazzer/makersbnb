from datetime import datetime

class AvailableRange:
    
    def __init__(self, availability_id, start_range, end_range, space_id):
        if isinstance(start_range, str) and isinstance(end_range, str):
            start = datetime.strptime(start_range, "%Y-%m-%d").date()
            end = datetime.strptime(end_range, "%Y-%m-%d").date()
            assert start < end, 'bad date, start cannot be bigger than end date'
            self.availability_id = availability_id
            self.start_range = start
            self.end_range = end
            self.space_id = space_id
        else:
            self.availability_id = availability_id
            self.start_range = start_range
            self.end_range = end_range
            self.space_id = space_id    

        
    @staticmethod
    def from_rowdict(rowdict):
        return AvailableRange(rowdict["availability_id"], rowdict["start_range"], rowdict["end_range"], rowdict["space_id"])


    def contains(self, start_date, end_date):
        assert start_date < end_date, 'bad date, start cannot be bigger than end date'

        return (self.start_range <= start_date <= self.end_range) \
        and (self.end_range >= end_date)

    def __repr__(self):
        return f"AvailableRange(availability_id = {self.availability_id}, " \
        f"start_range = {self.start_range}, " \
        f"end_range = {self.end_range}, "\
        f"space_id = {self.space_id})"

    def __eq__(self, other):
        return self.availability_id == other.availability_id \
        and self.start_range == other.start_range \
        and self.end_range == other.end_range \
        and self. space_id == other.space_id
