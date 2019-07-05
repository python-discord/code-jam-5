class ReminderTime:
    @classmethod
    def from_timestamp(cls, timestamp: str):
        hours, minutes = map(int, timestamp.split(':'))
        return cls(hours, minutes)

    @classmethod
    def from_minutes(cls, minutes: int):
        hours, minutes = divmod(minutes, 60)
        return cls(hours, minutes)

    def __init__(self, hours, minutes):
        self.hours = hours
        self.minutes = minutes

    def __str__(self):
        return f'{self.hours:02}:{self.minutes:02}'

    def __int__(self):
        return self.hours*60 + self.minutes
