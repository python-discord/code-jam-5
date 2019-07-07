from thoughtful_termites.app import qt

from .goal_list import GoalList
from .goal_list import GoalListItem
from .edit_goal_window import EditGoalWindow

from thoughtful_termites.shared.goal_db import (
    GoalDB,
    Goal,
    # Reminder,
    # ReminderTime,
    # Days
)

from thoughtful_termites.shared.constants import get_db


class GoalListWindow(qt.QWidget):
    def __init__(self):
        super().__init__()

        self.db: GoalDB = get_db()
        self.goal_list = GoalList(self.db)

        self.add_goal_button = qt.QPushButton()
        self.add_goal_button.setText('Add Goal')
        self.add_goal_button.clicked.connect(
            self.on_add_goal
        )

        self.main_layout = qt.QVBoxLayout(self)
        """
        The layout containing all this window's widgets.
        """
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addWidget(self.goal_list)
        self.main_layout.addWidget(self.add_goal_button)

        self.setWindowTitle('Goal List')

        for goal in self.db.get_goals():
            self.goal_list.addItem(
                GoalListItem(goal)
            )

    def on_add_goal(self):
        window = EditGoalWindow(self)

        def on_done():
            goal = Goal.create_new(
                self.db,
                window.name_box.text(),
                window.desc_box.text()
            )

            item = GoalListItem(goal)
            self.goal_list.addItem(item)

            window.done(0)

        window.done_button.clicked.connect(
            on_done
        )

        window.exec()
