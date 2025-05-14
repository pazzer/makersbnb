from lib.available_range import AvailableRange

class AvailableRangeRepo:
    def __init__(self, connection):
        self.connection = connection

    def list(self):
        rows = self.connection.execute('SELECT * FROM availabileRanges')
        available_ranges = []
        for row in rows:
            item = AvailableRange(row['availability_id'], row['start_range'],
                row['end_range'], row['space_id'])
            available_ranges.append(item)
        return available_ranges

    def add(self, available_range):
        self.connection.execute(f"INSERT INTO availabileRanges (start_range, " \
            "end_range, space_id) VALUES(%s,%s,%s)", [available_range.start_range, 
                available_range.end_range, available_range.space_id])
