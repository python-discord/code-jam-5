from .. import qt
from ..goal_suggestions import get_suggestion


class EditGoalWindow(qt.QDialog):
    def __init__(self, parent):
        super().__init__(parent)

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

        self.set_reminders_button.clicked.connect(
            self.on_set_reminders
        )

        self.get_suggestion_button = qt.QPushButton()
        self.get_suggestion_button.setText(
            'Suggest Goal'
        )

        self.get_suggestion_button.clicked.connect(
            self.on_get_suggestion
        )

        self.done_button = qt.QPushButton()
        self.done_button.setText(
            'Done'
        )

        self.done_button.setDefault(True)

        self.main_layout = qt.QVBoxLayout(self)
        """
        The layout containing all this window's widgets.
        """
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.name_box)
        self.main_layout.addWidget(self.desc_box)
        # self.main_layout.addWidget(self.set_reminders_button)
        self.main_layout.addWidget(self.get_suggestion_button)
        self.main_layout.addWidget(self.done_button)

        self.setWindowTitle('Edit Goal')
        self.setMaximumHeight(0)
        self.setFixedWidth(480)
        self.setModal(True)

    def on_set_reminders(self):
        pass

    def on_get_suggestion(self):
        suggestion = get_suggestion()
        self.name_box.setText(suggestion.name)
        self.desc_box.setText(suggestion.desc)
