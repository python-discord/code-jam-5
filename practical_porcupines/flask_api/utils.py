import datetime
from practical_porcupines.utils import check_date


def get_datetime(date):
    """
    > Gets date
    - String: Date
    < Returns datetime object
    x Returns DateFormatError if passed date is bad
    x Returns DatesOutOfRange if dates exceed dataset
    """

    date_full = check_date(date)

    return datetime.datetime(
        date_full[0][0],  # year
        date_full[0][1],  # month
        date_full[0][2],  # day
        date_full[1][0],  # hour
        date_full[1][1],  # minute
        date_full[1][2],  # second
    )
