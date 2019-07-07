from thoughtful_termites.shared import qt


class EditDailyReminderWindow(qt.QDialog):
    """
    This class describes a widget used to edit/add/describe a daily
    reminder.
    """
    def __init__(self, parent: qt.QWidget):
        super().__init__(parent)

        self.time_box = qt.QTimeEdit()
        """
        The box used to input the reminder time.
        """
        self.time_box.setTimeRange(
            qt.QTime(0, 0),
            qt.QTime(23, 59),
        )

        self.done_button = qt.QPushButton()
        """
        The button that signifies the user is done working inside this
        window and its effects should be applied.
        """
        self.done_button.setDefault(True)
        self.done_button.setText(
            'Done'
        )

        self.main_layout = qt.QVBoxLayout(self)
        """
        The layout containing all this window's widgets.
        """
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.time_box)
        self.main_layout.addWidget(self.done_button)

        self.setModal(True)
        self.setWindowTitle('Edit Daily Reminder')
