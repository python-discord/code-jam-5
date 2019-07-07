import asyncio
import datetime
import sqlite3

from functools import partial
from pathlib import Path
from typing import Union

from .goal import Goal
from .reminder import Reminder
from .reminder_day import ReminderDay
from .reminder_time import ReminderTime
from .unlocks import Unlock
from .farmertown import FarmerTownMain, FarmerTownDecision

cd = Path(__file__).parent
creation_script_path = cd / 'create_goal_db.sqlite'
"""
script used to create the goals/reminders database
"""


class GoalDB:
    """
    This class describes the database of all goals/reminders.
    """

    def __init__(self, loop: asyncio.BaseEventLoop = None):
        self.connection: sqlite3.Connection = None
        self.loop = loop or asyncio.get_event_loop()

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
        result.connection.execute('PRAGMA foreign_keys=ON;')
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
        await loop.run_in_executor(None, partial(self.new_goal, goal))

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

    def get_reminders(self, order=False):
        """
        A generator that yields all the reminders in the database

        :param: order: whether to order results by day and time (respectively).
        :returns: All the reminders in the database.
        """
        if order:
            query = "SELECT * FROM reminders ORDER BY day, time;"
        else:
            query = "SELECT * FROM reminders;"

        result = self.connection.execute(query)
        for row in result:
            yield Reminder.from_row(self, row)

    async def get_reminders_async(self, order=False):
        for reminder in self.get_reminders(order):
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

    def get_goal_by_name(self, goal_name):
        """Returns a goal by it's name.

        :param: goal_name: The name of the goal.
        :return: Goal with given name.
        """
        result = self.connection.execute(
            "SELECT * FROM goals WHERE name=?", (goal_name,)
        )
        for row in result:
            return Goal.from_row(self, row)

    async def get_goal_by_name_async(self, goal_name):
        """Coroutine helper to get a goal by name.

        :param: goal_name: The name of the goal
        :return: Goal with the given name"""
        return await self.loop.run_in_executor(
            None, partial(self.get_goal_by_name, goal_name)
        )

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

    async def get_reminder_by_id_async(self, id):
        """Coroutine helper to get reminder by ID

        :param: id: ID of the reminder.
        :return: Reminder with the given ID.
        """
        return await self.loop.run_in_executor(
            None, partial(self.get_reminder_by_id, id)
        )

    def get_reminder_by_goal_name(self, goal_name):
        """Returns a reminder for goal name passed.

        :param: goal_name: the goal name of the reminder.
        :return: Reminder with the given goal name.
        """

        result = self.connection.execute(
            'SELECT * FROM reminders INNER JOIN goals '
            'ON goals.id = reminders.goal_id WHERE goals.name=?',
            (goal_name,)
        )

        for row in result:
            return Reminder.from_row(self, row)

    async def get_reminder_by_goal_name_async(self, goal_name):
        """Coroutine helper to get a reminder for goal name passed.

        :param: goal_name: the goal name of the reminder.
        :return: Reminder with the given goal name.
        """
        return await self.loop.run_in_executor(
            None, partial(self.get_reminder_by_goal_name, goal_name)
        )

    def get_reminder_by_goal_id(self, goal_id):
        """Get a reminder with given goal ID

        :param: goal_id: The goal ID of the reminder.
        :return: Reminder with the given goal ID
        """

        result = self.connection.execute(
            "SELECT * FROM reminders WHERE goal_id=?", (goal_id, )
        )

        for row in result:
            return Reminder.from_row(self, row)

    async def get_reminder_by_goal_id_async(self, goal_id):
        """Coroutine helper to get a goal with given ID

        :param: goal_id: The goal ID of the reminder.
        :return: Reminder with the given goal ID
        """
        return await self.loop.run_in_executor(
            None, partial(self.get_reminder_by_goal_id, goal_id)
        )

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

    def get_next_reminder(self):
        """Get the next occurring reminder.
        """
        now = datetime.datetime.now()
        now_int = int(ReminderTime.from_timestamp(now.strftime('%H:%M')))

        result = self.connection.execute(
            "SELECT * FROM reminders WHERE day>=? AND time>=? "
            "ORDER BY day, time LIMIT 1;",
            (now.isoweekday(), now_int)
        )

        for row in result:
            return Reminder.from_row(self, row)

    async def get_next_reminder_async(self):
        """Coroutine helper to get the next reminder."""
        return await self.loop.run_in_executor(None, self.get_next_reminder)

    def get_unlocks(self):
        result = self.connection.execute("SELECT * FROM unlocks")

        for row in result:
            yield Unlock.from_row(self, row)

    def get_unlock_by_id(self, unlock_id):
        result = self.connection.execute("SELECT * FROM unlocks WHERE id=?", (unlock_id, ))

        for row in result:
            return Unlock.from_row(self, row)

    def get_unlock_by_name(self, name):
        result = self.connection.execute("SELECT * FROM unlocks WHERE name=?", (name, ))

        for row in result:
            return Unlock.from_row(self, row)

    async def create_farm(self, user_id, farmer_name):
        """Create a farmer town account with given user id and farmer name.
        :param: user_id: The user id to create account for.
        :param: farmer_name: The user's farmer name.
        """
        def execute():
            self.connection.execute("INSERT INTO farmertown (user_id, farmer_name) "
                                    "VALUES (?, ?)", (user_id, farmer_name))
            self.connection.commit()

        await self.loop.run_in_executor(None, execute)

    async def get_farmertown(self, user_id):
        """Get a FarmerTown account for a given user_id
        :param: user_id: The user id to fetch account for.
        :return: :class:`FarmerTownMain` - the farmer town account.
        """
        def fetch():
            return self.connection.execute("SELECT * FROM farmertown WHERE user_id=?", (user_id, ))
        result = await self.loop.run_in_executor(None, fetch)
        for row in result:
            return FarmerTownMain(self, row)

