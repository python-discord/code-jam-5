from thoughtful_termites.app import qt

from .reminder_list import ReminderList
from .add_reminder_window import AddReminderWindow

active_reminder_windows = set()


class ReminderListWindow(qt.QDialog):
    def __init__(self, parent: qt.QWidget):
        super().__init__(parent)

        self.reminder_list = ReminderList()

        self.add_reminder_button = qt.QPushButton()
        self.add_reminder_button.setText('Add Reminder')
        self.add_reminder_button.clicked.connect(
            self.on_add_reminder
        )

        self.main_layout = qt.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addWidget(self.reminder_list)
        self.main_layout.addWidget(self.add_reminder_button)

        self.setWindowTitle('Reminder List')
        self.setModal(True)

    def on_add_reminder(self):
        add_reminder_window = AddReminderWindow(self)

        def add_reminder_callback(window: AddReminderWindow):
            def callback():
                item = qt.QListWidgetItem(
                    f'{window.day_box.currentText()} - '
                    f'{window.time_box.date().toString()}'
                )

                self.reminder_list.addItem(item)
                window.done(0)

            return callback

        add_reminder_window.done_button.clicked.connect(
            add_reminder_callback(add_reminder_window)
        )
        active_reminder_windows.add(add_reminder_window)
        add_reminder_window.exec()
