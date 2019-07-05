import asyncio
import sqlite3

from pathlib import Path
from typing import Union

from .goal import Goal
from .reminder import Reminder
from .reminder_day import ReminderDay

cd = Path(__file__).parent
creation_script_path = cd/'create_goal_db.sqlite'
"""
script used to create the goals/reminders database
"""


class GoalDB:
    """
    This class describes the database of all goals/reminders.
    """

    def __init__(self):
        self.connection: sqlite3.Connection = None

    @classmethod
    def create_new(cls, path):
        """
        Create a new goal/reminder database at given path.
        All existing data will be wiped.

        :param path: Path of new database.
        :return: New database.
        """
        result = cls.load_from(path)

        cursor = result.connection.cursor()

        with open(creation_script_path) as script:
            cursor.executescript(script.read())

        result.connection.commit()
        cursor.close()

        return result

    @classmethod
    async def create_new_async(cls, path):
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, cls.create_new, path)
        return result

    @classmethod
    def load_from(cls, path):
        """
        Load goal/reminder database at given path.

        :param path: Path of database.
        :return: Database.
        """
        result = cls()
        result.connection = sqlite3.connect(
            path,
            check_same_thread=False,
            timeout=30,
        )
        result.connection.row_factory = sqlite3.Row
        return result

    @classmethod
    async def load_from_async(cls, path):
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, cls.load_from, path)
        return result

    def new_goal(self, name, desc):
        """
        Add a new goal to the database.

        :param name: Name of goal.
        :param desc: Description of goal.
        :return: Goal object used for storing/editing it.
        """
        return Goal.create_new(self, name, desc)

    async def new_goal_async(self, goal: Goal):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.new_goal, goal)

    def get_goals(self):
        """
        A generator that yields all the goals in the database

        :returns: All the goals in the database.
        """
        result = self.connection.execute('select * from goals')
        for row in result:
            yield Goal.from_row(self, row)

    async def get_goals_async(self):
        for goal in self.get_goals():
            yield goal

    def get_reminders(self):
        """
        A generator that yields all the reminders in the database

        :returns: All the reminders in the database.
        """
        result = self.connection.execute('select * from reminders')
        for row in result:
            yield Reminder.from_row(self, row)

    async def get_reminders_async(self):
        for reminder in self.get_reminders():
            yield reminder

    def get_goal_by_id(self, id):
        """
        Returns a goal by its ID.

        :param id: ID of goal.
        :return: Goal with given ID,
                or None if there is no goal with that ID.
        """
        result = self.connection.execute(
            'select * from goals where id=?', (id,)
        )

        for row in result:
            return Goal.from_row(self, row)

    def get_reminder_by_id(self, id):
        """
        Returns a reminder by its ID.

        :param id: ID of reminder.
        :return: Reminder with given ID,
                or None if there is no reminder with that ID.
        """
        result = self.connection.execute(
            'select * from reminders where id=?', (id,)
        )

        for row in result:
            return Reminder.from_row(self, row)

    def get_reminders_on_day(self, day: Union[int, str, ReminderDay]):
        """
        Generator that yields all reminders on a given day.

        :param day: Day of reminders.
        :return: Reminders on the given day.
        """
        if isinstance(day, int):
            day = ReminderDay.from_int(day)
        elif isinstance(day, str):
            day = ReminderDay(day)

        result = self.connection.execute(
            'select * from reminders where day=?', (int(day),)
        )

        for row in result:
            yield Reminder.from_row(self, row)

    async def get_reminders_on_day_async(
            self,
            day: Union[int, str, ReminderDay]
    ):
        for reminder in self.get_reminders_on_day(day):
            yield reminder
