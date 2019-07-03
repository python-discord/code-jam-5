import datetime
from typing import Union

def string_to_datetime(date_string: str) -> Union[datetime.datetime, None]:
    """
    > Func to convert stings in format '%Y:%m:%d:%H:%M:%S' to datetime
      Example:
            string_to_datetime('2010:06:29:17:02:39')
            > datetime.datetime(2010, 6, 29, 17, 2, 39)
            - possible_formats: '2019:06:26:06:26:33', '06:26:33 26.06.2019',
            - '06/26/2019 06:26:33', '26.06.2019', 06/26/2019, 2019-06-29 23:02:05
    - date_string: The string that should be converted
    < Returns Corresponding datetime object
    < Returns If it will be a prediction or not
    x Returns DateFormatError if incoming string isn\'t properly formatted
    """

    possible_formats = [
        "%Y",
        "%Y-%m",
        "%Y/%m",
        "%Y:%m:%d:%H:%M:%S",
        "%H:%M:%S %d.%m.%Y",
        "%m/%d/%Y %H:%M:%S",
        "%d.%m.%Y",
        "%m/%d/%Y",
        "%Y-%m-%d %H:%M:%S",
    ]

    possible_dates = list()

    for possible_format in possible_formats:
        try:
            possible_dates.append(
                datetime.datetime.strptime(date_string, possible_format)
            )
        except ValueError:
            pass

    if possible_dates:
        date = [date for date in possible_dates][0]
    else:
        date = None

    if not date:
        raise DateFormatError(
            "Datetime %Y must have 4 digits, add `0`\'s to the front of date!"
        )

    is_prediction = False

    if datetime.date(1993, 1, 15) > date.date() or datetime.date(2019, 2, 7) < date.date():
        raise PredictionNotImplamentedError(
            "Predictions are not implamented at this current time!"
        )
        
        is_prediction = True

    return date, is_prediction