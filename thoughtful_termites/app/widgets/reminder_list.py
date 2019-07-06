from thoughtful_termites.app import qt
from thoughtful_termites.shared.goal_db import Goal
from thoughtful_termites.shared.goal_db import Reminder
from thoughtful_termites.shared.goal_db import ReminderDay
from thoughtful_termites.shared.goal_db import ReminderTime
from .edit_reminder_window import EditReminderWindow


class ReminderListItem(qt.QListWidgetItem):
    def __init__(self, reminder: Reminder):
        super().__init__()

        self.reminder = reminder
        self.setText(
            f'{reminder.day} {reminder.time}'
        )


class ReminderList(qt.QListWidget):
    def __init__(self, goal: Goal):
        super().__init__()

        self.setContextMenuPolicy(qt.constants.CustomContextMenu)
        self.customContextMenuRequested.connect(
            self.on_context_menu
        )

        self.setSelectionMode(self.ExtendedSelection)

        self.goal = goal

        for reminder in goal.get_reminders():
            item = ReminderListItem(reminder)
            self.addItem(item)

    def on_context_menu(self, pos: qt.QPoint):
        item: ReminderListItem = self.itemAt(pos)
        selected_items = self.selectedItems()

        def on_edit():
            edit_reminder_window = EditReminderWindow(self.window())
            edit_reminder_window.time_box.setTime(
                qt.QTime(
                    item.reminder.time.hours,
                    item.reminder.time.minutes,
                )
            )
            edit_reminder_window.day_box.setCurrentIndex(
                edit_reminder_window.day_box.findText(
                    item.reminder.day.name
                )
            )

            def on_done():
                time = edit_reminder_window.time_box.time().toPyTime()
                time = f'{time.hour}:{time.minute}'
                day = edit_reminder_window.day_box.currentText()

                item.reminder.time = ReminderTime.from_timestamp(
                    time
                )

                item.reminder.day = ReminderDay(day)
                item.reminder.update()

                item.setText(
                    f'{item.reminder.day} {item.reminder.time}'
                )

                edit_reminder_window.done(0)

            edit_reminder_window.done_button.clicked.connect(
                on_done
            )
            edit_reminder_window.exec()

        def on_delete():
            for item in selected_items:  # type: ReminderListItem
                item.reminder.delete()
                self.takeItem(self.row(item))

        if item:
            menu = qt.QMenu()
            menu.addAction('Edit', on_edit)
            menu.addAction('Delete', on_delete)

            menu.exec(self.mapToGlobal(pos))
