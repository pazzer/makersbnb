from lib.space import Space
from lib.available_range import *
from lib.user_repository import UserRepository

class SpaceRepository:
    def __init__(self, _connection):
        self._connection = _connection

    def list_spaces(self):
        rows = self._connection.execute('SELECT * FROM spaces')
        spaces = []

        for row in rows:
            item = Space(row['space_id'], row['name'], row['description'], row['price_per_night'], row['img_filename'], row['user_id'])
            spaces.append(item)
        return spaces

    def list_spaces_by_date_range(self, holiday_start, holiday_end):
        '''
        1) need to check that the supplied dates fall within the available range for a property [done]
        2) take our results from the first filter and look at every booking and check that our date range doesen't overlap
        '''

        available_spaces = []
        for space in self.list_spaces():
            rows = self._connection.execute("SELECT * FROM available_ranges WHERE space_id = %s ", [space.space_id])
            if len(rows) == 0:
                available_spaces.append(space)
            else:
                available_range = AvailableRange.from_rowdict(rows[0])
                if available_range.contains(holiday_start, holiday_end):
                    available_spaces.append(space)
        return available_spaces


    def add_space(self, space):
        rows = self._connection.execute(
            'INSERT INTO spaces (name, description, price_per_night, img_filename, user_id) VALUES (%s, %s, %s, %s, %s) RETURNING space_id',
            [space.name, space.description, space.price_per_night, space.img_filename, space.user_id])
        row = rows[0]
        space.space_id = row['space_id']
        return space.space_id

    def find(self, space_id):
        rows = self._connection.execute(
            'SELECT * from spaces WHERE space_id = %s', [space_id])
        row = rows[0]
        return Space(row["space_id"], row["name"], row["description"], row["price_per_night"], row["img_filename"], row["user_id"])
    
    def find_for_user(self, user_id):
        rows = self._connection.execute(
            'SELECT * from spaces WHERE user_id = %s', [user_id])

        return [Space(row["space_id"], row["name"], row["description"], row["price_per_night"], row["img_filename"], row["user_id"]) for row in rows]



    def spaces_and_owners_for_dates(self, lower_bound, upper_bound):
        spaces = self.list_spaces_by_date_range(lower_bound, upper_bound)
        user_repository = UserRepository(self._connection)
        owners = [user_repository.find_by_id(space.user_id) for space in spaces]
        return spaces, owners


