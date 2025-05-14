from lib.space import Space
from lib.available_range import *

class SpaceRepository:
    def __init__(self, _connection):
        self._connection = _connection

    def list_spaces(self):
        rows = self._connection.execute('SELECT * FROM spaces')
        spaces = []

        for row in rows:
            item = Space(row['space_id'], row['name'], row['description'], row['price_per_night'], row['user_id'])
            spaces.append(item)
        return spaces

    def list_spaces_by_date_range(self, holiday_start, holiday_end):
        '''
        1) need to check that the supplied dates fall within the available range for a property [done]
        2) take our results from the first filter and look at every booking and check that our date range doesen't overlap 
        '''

        available_spaces = []
        for space in self.list_spaces():
            rows = self._connection.execute("SELECT * FROM availabileRanges WHERE space_id = %s ", [space.space_id])
            available_range = AvailableRange.from_rowdict(rows[0])
            if available_range.contains(holiday_start, holiday_end):
                available_spaces.append(space)
        return available_spaces


    def add_space(self, space):
        self._connection.execute(
            'INSERT INTO spaces (name, description, price_per_night, user_id) VALUES (%s, %s, %s, %s)',
            [space.name, space.description, space.price_per_night, space.user_id])
        return None

    def find(self, space_id):
        rows = self._connection.execute(
            'SELECT * from spaces WHERE space_id = %s', [space_id])
        row = rows[0]
        return Space(row["space_id"], row["name"], row["description"], row["price_per_night"], row["user_id"])
    
    def find_for_user(self, user_id):
        rows = self._connection.execute(
            'SELECT * from spaces WHERE user_id = %s', [user_id])
        return [Space(row["space_id"], row["name"], row["description"], row["price_per_night"], row["user_id"]) for row in rows]