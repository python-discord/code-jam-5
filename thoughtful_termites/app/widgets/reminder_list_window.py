from thoughtful_termites.shared import qt

from .reminder_list import ReminderList
from .reminder_list import ReminderListItem
from .edit_reminder_window import EditReminderWindow
from .edit_daily_reminder_window import EditDailyReminderWindow

from thoughtful_termites.shared.goal_db import Goal
from thoughtful_termites.shared.goal_db.reminder_day import day_to_int


class ReminderListWindow(qt.QDialog):
    def __init__(self, parent: qt.QWidget, goal: Goal):
        super().__init__(parent)

        self.goal = goal
        self.reminder_list = ReminderList(goal)

        self.add_reminder_button = qt.QPushButton()
        self.add_reminder_button.setText('Add Reminder')
        self.add_reminder_button.clicked.connect(
            self.on_add_reminder
        )

        self.add_daily_reminder_button = qt.QPushButton()
        self.add_daily_reminder_button.setText('Add Daily Reminder')
        self.add_daily_reminder_button.clicked.connect(
            self.on_add_daily_reminder
        )

        self.main_layout = qt.QVBoxLayout(self)
        """
        The layout containing all this window's widgets.
        """
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addWidget(self.reminder_list)
        self.main_layout.addWidget(self.add_reminder_button)
        self.main_layout.addWidget(self.add_daily_reminder_button)

        self.setWindowTitle('Reminder List')
        self.setModal(True)

    def on_add_reminder(self):
        window = EditReminderWindow(self)

        def callback():
            time = window.time_box.time().toPyTime()
            time = f'{time.hour}:{time.minute}'
            day = window.day_box.currentText()

            reminder = self.goal.new_reminder(
                day, time
            )

            item = ReminderListItem(reminder)
            self.reminder_list.addItem(item)
            window.done(0)

        window.done_button.clicked.connect(callback)
        window.exec()

    def on_add_daily_reminder(self):
        window = EditDailyReminderWindow(self)

        def callback():
            time = window.time_box.time().toPyTime()
            time = f'{time.hour}:{time.minute}'

            for day in day_to_int.keys():
                reminder = self.goal.new_reminder(
                    day, time
                )
                item = ReminderListItem(reminder)
                self.reminder_list.addItem(item)

            window.done(0)

        window.done_button.clicked.connect(callback)
        window.exec()
