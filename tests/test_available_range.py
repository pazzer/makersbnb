from datetime import datetime
from lib.available_range import AvailableRange
import pytest

spring = ('2025-03-01','2025-06-01')
summer = ('2025-06-01','2025-09-01')
autumn = ('2025-09-01','2025-12-01')
winter = ('2025-12-01','2026-03-01')

def str_to_date(the_string):
    return datetime.strptime(the_string, "%Y-%m-%d").date()

'''
this class will have a:
availability_id
start_range
end_range
space_id
'''
def test_available_range_constructor():
    ar = AvailableRange(1,summer[0],summer[1],5)
    assert ar.start_range == datetime.strptime(summer[0], "%Y-%m-%d").date()
    assert ar.end_range == datetime.strptime(summer[1], "%Y-%m-%d").date()
    assert ar.space_id == 5

'''
this will check if the dates given are contained
within the available range

we assume that we are always passing DATE objects
never strings
'''

def test_available_range_does_contain_passed_dates():
    property_available = summer[0], summer[1]
    my_annual_leave = str_to_date('2025-07-18'), str_to_date('2025-07-25')
    ar = AvailableRange(2,property_available[0], property_available[1],10)
    does_contain = ar.contains(my_annual_leave[0],my_annual_leave[1])
    assert does_contain == True

def test_available_range_does_not_contain_passed_dates():
    property_available = summer[0], summer[1]
    my_annual_leave = str_to_date('2025-07-18'), str_to_date('2030-07-25')
    ar = AvailableRange(8,property_available[0], property_available[1],10)
    does_contain = ar.contains(my_annual_leave[0],my_annual_leave[1])
    assert does_contain == False


'''
test that the assert statement get trown
'''

def test_assert_statement_get_thrown_if_startdate_bigger_than_end():
    with pytest.raises(Exception) as e:
        ar = AvailableRange(9,winter[1], winter[0],-500)
    assert str(e.value) == 'bad date, start cannot be bigger than end date'