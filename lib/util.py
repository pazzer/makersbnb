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
        assert False, 'bad separator - expected "-" or "/"'

    return datetime.strptime(stringdate, separator.join(fmt_comps)).date()



def date_to_str(date_):
    return date_.strftime('%Y/%m/%d')


