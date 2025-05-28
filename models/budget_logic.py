from datetime import datetime, timedelta, date

def get_budget_period(today=None):
    if today is None:
        today = date.today()
    # Om dagen är 25 eller senare, starta från denna månads 25:e till nästa månads 24:e
    if today.day >= 25:
        period_start = today.replace(day=25)
        # Hantera årsskifte
        if today.month == 12:
            period_end = date(today.year + 1, 1, 24)
        else:
            period_end = date(today.year, today.month + 1, 24)
    else:
        # Starta från förra månaden 25:e till denna månads 24:e
        if today.month == 1:
            period_start = date(today.year - 1, 12, 25)
        else:
            period_start = date(today.year, today.month - 1, 25)
        period_end = today.replace(day=24)
    return period_start, period_end