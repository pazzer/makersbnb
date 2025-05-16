from lib.available_range import AvailableRange
from lib.available_range_repo import AvailableRangeRepo
from datetime import datetime
summer = ('2025-06-01','2025-09-01')


'''
when we call the #list it will return 
all the available ranges
'''
def test_available_range_repo_list(db_connection):
    db_connection.seed('seeds/makersbnb.sql')
    repository = AvailableRangeRepo(db_connection)
    available_ranges = repository.list() #get all available ranges
    assert available_ranges == [
        AvailableRange(1,'2025-04-15', '2026-05-01', 1),
        AvailableRange(2,'2025-05-01', '2026-05-01', 2),
        AvailableRange(3,'2025-05-01', '2026-05-01', 3),
        AvailableRange(4,'2025-05-01', '2026-05-01', 4),
        AvailableRange(5,'2025-04-15', '2026-05-01', 5),
        AvailableRange(6,'2025-04-15', '2026-06-01', 6)
        ]


'''
when we call #add we are able to add a new set of available range
to the database
'''

def test_add_available_range(db_connection):
    db_connection.seed('seeds/makersbnb.sql')
    repository = AvailableRangeRepo(db_connection)

    available_range = AvailableRange(None, summer[0], summer[1],6)
    repository.add(available_range)

    assert repository.list() == [
        AvailableRange(1,'2025-04-15', '2026-05-01', 1),
        AvailableRange(2,'2025-05-01', '2026-05-01', 2),
        AvailableRange(3,'2025-05-01', '2026-05-01', 3),
        AvailableRange(4,'2025-05-01', '2026-05-01', 4),
        AvailableRange(5,'2025-04-15', '2026-05-01', 5),
        AvailableRange(6,'2025-04-15', '2026-06-01', 6),
        AvailableRange(7,f'{summer[0]}', f'{summer[1]}',6)
        ]
