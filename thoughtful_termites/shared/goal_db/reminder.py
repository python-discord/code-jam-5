import asyncio
import sqlite3
import weakref

from functools import partial
from typing import TYPE_CHECKING, Union

from .reminder_time import ReminderTime
from .reminder_day import ReminderDay

if TYPE_CHECKING:
    from .db import GoalDB
    from .goal import Goal


class Reminder:
    """
    This class describes individual reminders stored in a reminder database.
    """
    def __init__(self):
        self.id: int = None
        """
        ID of the reminder in the database.
        """

        self.goal_id: int = None
        """
        ID of the goal to which this reminder belongs.
        """

        self.day: ReminderDay = None
        """
        Day of the reminder.
        """

        self.time: ReminderTime = None
        """
        Time of the reminder.
        """

        self.db_ref: weakref.ref = None
        """
        Weak reference to the database object which created this object.
        """
        self.loop = asyncio.get_event_loop()
        """
        Asyncio loop to run blocking calls.
        """

    @classmethod
    def from_row(cls, db: 'GoalDB', row: sqlite3.Row):
        """
        Create and return a new reminder object from a row returned as a
        result of a query.

        :param db: The GoalDB generating this object.
        :param row: The row containing reminder data.
        :return: The Reminder object representing the data.
        """

        result = cls()

        result.id = row['id']
        result.goal_id = row['goal_id']

        result.day = ReminderDay.from_int(row['day'])
        result.time = ReminderTime.from_minutes(row['time'])

        result.db_ref = weakref.ref(db)

        return result

    @classmethod
    def create_new(
            cls,
            goal: 'Goal',
            day: Union[int, str, ReminderTime],
            time: Union[int, str, ReminderDay]
    ):
        """
        Create and return a new goal object based on a given name and
        description.

        :param goal: The goal to which this reminder should belong.
        :param day: The day of the reminder.
        :param time: The time of the reminder.
        :return: The new reminder.
        """

        if isinstance(time, int):
            time = ReminderTime.from_minutes(time)
        elif isinstance(time, str):
            time = ReminderTime.from_timestamp(time)

        if isinstance(day, int):
            day = ReminderDay.from_int(day)
        elif isinstance(day, str):
            day = ReminderDay(day)

        cursor = goal.db.connection.cursor()
        cursor.execute(
            'insert into reminders (day, time, goal_id) values (? ,?, ?)',
            (int(day), int(time), goal.id)
        )

        goal.db.connection.commit()
        cursor.close()

        result = cls()
        result.id = cursor.lastrowid
        result.goal_id = goal.id
        result.day = day
        result.time = time
        result.db_ref = goal.db_ref

        return result

    @property
    def db(self) -> 'GoalDB':
        """
        A convenience property for dereferencing the goal DB weakref.

        :return: The actual GoalDB containing this reminder.
        """
        return self.db_ref()

    def delete(self, commit=True):
        """
        Remove this reminder from the database.

        :param commit: If true, the change will be immediately
        committed.
        """
        cursor = self.db.connection.execute(
            'delete from reminders where id=?', (self.id,)
        )

        if commit:
            self.db.connection.commit()
            cursor.close()

    async def delete_async(self):
        return await self.loop.run_in_executor(None, partial(self.delete))

    @property
    def goal(self):
        """
        Convenience property for getting the goal to which this
        reminder belongs from the database.

        :return: The goal to which this reminder belongs.
        """
        return self.db.get_goal_by_id(self.goal_id)

    def update(self, commit=True):
        """
        Apply any changes to this reminder to the database.

        :param commit: If true, changes will be committed immediately.
        """
        cursor = self.db.connection.execute(
            'update reminders '
            'set day=?, '
            'set time=? '
            'where id=?',
            (int(self.day), int(self.time), self.id)
        )

        if commit:
            self.db.connection.commit()
            cursor.close()

    def __str__(self):
        return f'Reminder({self.goal}, {self.day}, {self.time})'
