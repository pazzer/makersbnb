from datetime import datetime

def to_date(stringdate):
    fmt_comps = ['%Y', '%m', '%d']
    if '/' in stringdate:
        separator = '/'
        comps = stringdate.split()
    elif '-' in stringdate:
        separator = '-'
        comps = stringdate.split()
    else:
        assert False, f'format "{stringdate}" not recognised'

    return datetime.strptime(stringdate, separator.join(fmt_comps)).date()



def date_to_str(date_):
    return date_.strftime('%Y-%m-%d')


def format_date_range(start, end):
    fmt_str = '%a %-d %b' if start.year == end.year else '%a %-d %b %y'
    return f"{ start.strftime(fmt_str) } - { end.strftime(fmt_str) }"


