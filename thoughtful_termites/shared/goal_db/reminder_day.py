day_to_int = {
    'Monday': 0,
    'Tuesday': 1,
    'Wednesday': 2,
    'Thursday': 3,
    'Friday': 4,
    'Saturday': 5,
    'Sunday': 6,
}

int_to_day = {
    value: key for key, value in day_to_int.items()
}


class ReminderDay:
    @classmethod
    def from_int(cls, int):
        return cls(int_to_day[int])

    def __init__(self, name):
        self.name = name

    def __int__(self):
        return day_to_int[self.name]

    def __str__(self):
        return self.name


class Days:
    Monday = ReminderDay('Monday')
    Tuesday = ReminderDay('Tuesday')
    Wednesday = ReminderDay('Wednesday')
    Thursday = ReminderDay('Thursday')
    Friday = ReminderDay('Friday')
    Saturday = ReminderDay('Saturday')
    Sunday = ReminderDay('Sunday')
