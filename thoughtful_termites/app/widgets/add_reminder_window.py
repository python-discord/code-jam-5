from .. import qt


class AddReminderWindow(qt.QDialog):
    def __init__(self, parent: qt.QWidget):
        super().__init__(parent)

        self.day_box = qt.QComboBox()
        self.day_box.addItem('Monday')
        self.day_box.addItem('Tuesday')
        self.day_box.addItem('Wednesday')
        self.day_box.addItem('Thursday')
        self.day_box.addItem('Friday')
        self.day_box.addItem('Saturday')
        self.day_box.addItem('Sunday')

        self.time_box = qt.QTimeEdit()
        self.time_box.setTimeRange(
            qt.QTime(0, 0),
            qt.QTime(23, 59),
        )

        self.done_button = qt.QPushButton()
        self.done_button.setDefault(True)
        self.done_button.setText(
            'Done'
        )

        self.main_layout = qt.QVBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.day_box)
        self.main_layout.addWidget(self.time_box)
        self.main_layout.addWidget(self.done_button)

        self.setModal(True)
        self.setWindowTitle('Edit Reminder')
