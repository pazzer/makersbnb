from lib.available_range import AvailableRange
from lib.available_range_repo import AvailableRangeRepo
from datetime import datetime
summer = ('2025-06-01','2025-09-01')


'''
when we call the #list it will return 
all the available ranges
'''
def test_album_repo_list(db_connection):
    db_connection.seed('seeds/makersbnb.sql')
    repository = AvailableRangeRepo(db_connection)
    avalable_ranges = repository.list() #get all available ranges
    assert avalable_ranges == [
        AvailableRange(1,'2025-06-01', '2025-06-10', 1),
        AvailableRange(2,'2025-06-05', '2025-06-15', 2),
        AvailableRange(3,'2025-07-01', '2025-07-10', 3),
        AvailableRange(4,'2025-07-15', '2025-07-25', 4),
        AvailableRange(5,'2025-08-01', '2025-08-10', 5)
        ]


'''
when we call #add we are able to add a new set of available range
to the database
'''

def test_add_available_range(db_connection):
    db_connection.seed('seeds/makersbnb.sql')
    repository = AvailableRangeRepo(db_connection)

    available_range = AvailableRange(None, summer[0], summer[1],5)
    repository.add(available_range)

    assert repository.list() == [
        AvailableRange(1,'2025-06-01', '2025-06-10', 1),
        AvailableRange(2,'2025-06-05', '2025-06-15', 2),
        AvailableRange(3,'2025-07-01', '2025-07-10', 3),
        AvailableRange(4,'2025-07-15', '2025-07-25', 4),
        AvailableRange(5,'2025-08-01', '2025-08-10', 5),
        AvailableRange(6,f'{summer[0]}', f'{summer[1]}',5)
        ]
