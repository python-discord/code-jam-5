from .. import qt


class AddGoalWindow(qt.QWidget):
    def __init__(self):
        super().__init__()

        self.name_box = qt.QLineEdit()
        self.name_box.setPlaceholderText(
            'Short name for goal. '
            'e.g. Drive Less'
        )

        self.desc_box = qt.QLineEdit()
        self.desc_box.setPlaceholderText(
            'Description of goal. '
            'e.g. Take public transportation or ride a bike on some days.'
        )

        self.set_reminders_button = qt.QPushButton()
        self.set_reminders_button.setText(
            'Set Goal Reminders'
        )

        self.get_suggestion_button = qt.QPushButton()
        self.get_suggestion_button.setText(
            'Suggest Goal'
        )

        self.done_button = qt.QPushButton()
        self.done_button.setText(
            'Done'
        )

        self.main_layout = qt.QVBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.name_box)
        self.main_layout.addWidget(self.desc_box)
        self.main_layout.addWidget(self.set_reminders_button)
        self.main_layout.addWidget(self.get_suggestion_button)
        self.main_layout.addWidget(self.done_button)
