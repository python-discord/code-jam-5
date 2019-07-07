import sqlite3
import weakref

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .db import GoalDB


class Unlock:
    def __init__(self):
        self.id: int = None
        self.name: str = None
        self.is_unlocked: bool = None

        self.db_ref: weakref.ref = None

    @classmethod
    def from_row(cls, db: 'GoalDB', row: sqlite3.Row):
        result = cls()

        result.id = row["id"]
        result.name = row["name"]
        result.is_unlocked = (row["is_unlocked"] == 1)
        result.db_ref = weakref.ref(db)

        return result

    @classmethod
    def create_new(cls, db: 'GoalDB', name, is_unlocked):
        cursor = db.connection.cursor()
        cursor.execute(
            "insert into unlocks (name, is_unlocked) values (?, ?)",
            (name, 1 if is_unlocked else 0)
        )

        db.connection.commit()
        cursor.close()

        result = cls()
        result.id = cursor.lastrowid
        result.name = name
        result.is_unlocked = is_unlocked
        result.db_ref = weakref.ref(db)

        return result

    @property
    def db(self) -> 'GoalDB':
        """
        A convenience property for dereferencing the goal DB weakref.

        :return: The actual GoalDB containing this goal.
        """
        return self.db_ref()

    def update(self, commit=True):
        """
        Apply any changes to this unlock to the database.

        :param commit: If true, changes will be committed immediately.
        """
        cursor = self.db.connection.execute(
            "update unlocks set (name, is_unlocked)=(?, ?) where id=?",
            (self.name, 1 if self.is_unlocked else 0, self.id)
        )

        if commit:
            self.db.connection.commit()
            cursor.close()
