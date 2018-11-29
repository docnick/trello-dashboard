import datetime


DATE_FORMAT = '%Y-%m-%d'


def get_today_date():
    today = datetime.datetime.now()
    today_date = datetime.date(today.year, today.month, today.day)
    return today_date


def is_date_today(date_in):
    return date_in == get_today_date()


def is_date_before_today(date_in):
    return date_in < get_today_date()


def is_before_close_business():
    today = datetime.datetime.now()
    if today.hour < 20:
        return True
    return False


def get_date_range(days_ago):
    today = get_today_date()
    start_date = today - datetime.timedelta(days=days_ago)

    current_date = start_date
    while current_date <= today:
        yield current_date
        current_date += datetime.timedelta(days=1)


def get_date(date_str):
    idx = date_str.find('T')
    if idx > 0:
        date_str = date_str[:idx]
    dt = datetime.datetime.strptime(date_str, DATE_FORMAT)
    return datetime.date(dt.year, dt.month, dt.day)


def get_created_on_date(item_id):
    return datetime.date.fromtimestamp(int(item_id[0:8], 16))


def date_diff_days(date_start, date_end=get_today_date()):
    return (date_end - date_start).days