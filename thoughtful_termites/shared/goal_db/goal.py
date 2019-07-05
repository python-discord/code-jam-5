import asyncio
import sqlite3
import weakref

from typing import TYPE_CHECKING, Union

from .reminder import Reminder

if TYPE_CHECKING:
    from .db import GoalDB
    from .reminder_day import ReminderDay
    from .reminder_time import ReminderTime


class Goal:
    """
    This class describes individual goals stored in a goal database.
    """
    def __init__(self):
        self.id: int = None
        """
        ID of goal in the database.
        """

        self.name: str = None
        """
        Name of goal.
        """

        self.desc: str = None
        """
        Description of goal.
        """

        self.db_ref: weakref.ref = None
        """
        Weak reference to the database object which created this object.
        """

    @classmethod
    def from_row(cls, db: 'GoalDB', row: sqlite3.Row):
        """
        Create and return a new goal object from a row returned as a
        result of a query.

        :param db: The GoalDB generating this object.
        :param row: The row containing goal data.
        :return: The Goal object representing the data.
        """

        result = cls()

        result.id = row['id']
        result.name = row['name']
        result.desc = row['desc']

        result.db_ref = weakref.ref(db)

        return result

    @classmethod
    def create_new(cls, db: 'GoalDB', name, desc):
        """
        Create and return a new goal object based on a given name and
        description.

        :param db: The GoalDB to which this goal should be added.
        :param name: The name of the goal.
        :param desc: The description of the goal.
        :return: The new goal.
        """
        cursor = db.connection.cursor()
        cursor.execute(
            'insert into goals (name, desc) values (? ,?)',
            (name, desc)
        )

        db.connection.commit()
        cursor.close()

        result = cls()
        result.id = cursor.lastrowid
        result.name = name
        result.desc = desc
        result.db_ref = weakref.ref(db)

        return result

    @property
    def db(self) -> 'GoalDB':
        """
        A convenience property for dereferencing the goal DB weakref.

        :return: The actual GoalDB containing this goal.
        """
        return self.db_ref()

    def get_reminders(self):
        """
        A generator that yields all reminders associated with this goal.

        :return: All reminders associated with this goal.
        """
        result = self.db.connection.execute(
            'select * from reminders where goal_id=?', (self.id,)
        )

        for row in result:
            yield Reminder.from_row(self.db, row)

    async def get_reminders_async(self):
        for goal in self.get_reminders():
            yield goal

    def delete(self, commit=True):
        """
        Remove this goal from the database.

        :param commit: If true, the change will be immediately
        committed.
        """
        cursor = self.db.connection.execute(
            'delete from goals where id=?', (self.id,)
        )

        if commit:
            self.db.connection.commit()
            cursor.close()

    async def delete_async(self):
        self.delete()
        await asyncio.sleep(0)

    def new_reminder(
            self,
            day: Union[int, str, 'ReminderDay'],
            time: Union[int, str, 'ReminderTime']
    ):
        """
        Create and return a new reminder for this goal at a given
        day and time.

        :param day: Day of the reminder.
        :param time: Time of the reminder.
        :return:
        """
        return Reminder.create_new(self, day, time)

    def update(self, commit=True):
        """
        Apply any changes to this goal to the database.
        This will not apply changes to its reminders.
        Those must be applied individually per reminder.

        :param commit: If true, changes will be committed immediately.
        """
        cursor = self.db.connection.execute(
            'update goals '
            'set name=?, '
            'set desc=? '
            'where id=?',
            (self.name, self.desc, self.id)
        )

        if commit:
            self.db.connection.commit()
            cursor.close()

    def __str__(self):
        return f'Goal ({self.name}, {self.desc})'
