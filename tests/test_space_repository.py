from lib.space_repository import SpaceRepository
from lib.space import Space
from lib.util import str_to_date

def space_name_in_list(_list, space_name):
    for space in _list:
        if space.name == space_name:
            return True
    return False




"""
When we call SpaceRepository #list_spaces
We get a list of Space objects reflecting the seed data.
"""
def test_get_all_spaces(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = SpaceRepository(db_connection)

    spaces = repository.list_spaces()

    assert spaces == [
        Space(1, 'Cozy Cabin', 'Rustic cabin in the forest.', 100, 1),
        Space(2, 'Urban Loft', 'Sleek apartment in downtown.', 150, 2),
        Space(3, 'Beach Bungalow', 'Sunny spot by the sea.', 200, 3),
        Space(4, 'Mountain Retreat', 'Quiet escape in the hills.', 180, 4),
        Space(5, 'Modern Studio', 'Compact yet luxurious.', 120, 5),
        Space(6, 'Cool Castle', 'Spacious but drafty.', 99, 6)
    ]

"""
When we call SpaceRepository #add_space
And then call #list_spaces
We get a list of spaces with the new space included
"""

def test_add_space(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = SpaceRepository(db_connection)

    new_space = Space(None, 'Cardboard Box', 'Back to basics, no ensuite.', 10000, 1)
    repository.add_space(new_space)
    
    spaces = repository.list_spaces()

    assert spaces == [
        Space(1, 'Cozy Cabin', 'Rustic cabin in the forest.', 100, 1),
        Space(2, 'Urban Loft', 'Sleek apartment in downtown.', 150, 2),
        Space(3, 'Beach Bungalow', 'Sunny spot by the sea.', 200, 3),
        Space(4, 'Mountain Retreat', 'Quiet escape in the hills.', 180, 4),
        Space(5, 'Modern Studio', 'Compact yet luxurious.', 120, 5),
        Space(6, 'Cool Castle', 'Spacious but drafty.', 99, 6),
        Space(7, 'Cardboard Box', 'Back to basics, no ensuite.', 10000, 1)
    ]


'''
1) need to check that the supplied dates fall within the available range for a property 
2) take our results from the first filter and look at every booking and check that our date range doesen't overlap 

cozy cabin ('2025-06-01', '2025-06-10', 1),
'''

def test_date_range_accepted_by_cozy_cabin(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = SpaceRepository(db_connection)

    holiday_start = str_to_date("2025-06-01")
    holiday_end = str_to_date("2025-06-10")

    result = repository.list_spaces_by_date_range(holiday_start,holiday_end)
    assert space_name_in_list(result, 'Cozy Cabin')
    assert len(result) == 1



def test_date_range_accepted_by_two(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = SpaceRepository(db_connection)

    holiday_start = str_to_date("2025-06-05")
    holiday_end = str_to_date("2025-06-10")

    result = repository.list_spaces_by_date_range(holiday_start,holiday_end)
    assert space_name_in_list(result, 'Cozy Cabin')
    assert space_name_in_list(result, 'Urban Loft')
    assert len(result) == 2


def test_date_range_has_no_matching_spaces(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    repository = SpaceRepository(db_connection)

    holiday_start = str_to_date("2016-06-05")
    holiday_end = str_to_date("2025-06-10")

    result = repository.list_spaces_by_date_range(holiday_start,holiday_end)
    assert len(result) == 0
