from datetime import datetime

def to_date(stringdate):
    return datetime.strptime(stringdate, '%Y/%m/%d').date()

def date_to_str(date_):
    return date_.strftime('%Y/%m/%d')


