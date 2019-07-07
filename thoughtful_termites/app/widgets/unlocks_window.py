from thoughtful_termites.shared import qt
from thoughtful_termites.shared.database import get_db
from thoughtful_termites.shared.constants import completed_goals_path


class UnlocksWindow(qt.QDialog):
    @staticmethod
    def set_completed_goals(n: int):
        """
        Update the number of goals completed by the user into completed_goals_path.

        :param n: The updated number of goals that have been completed by the user
        """
        with open(completed_goals_path, 'w') as f:
            f.write(str(n))

    @staticmethod
    def completed_goals():
        """
        Fetches the number of goals that the user has completed in completed_goals_path.
        If no such path exists, the user hasn't completed any goals so far.

        :return: The number of goals the user has completed
        """
        if completed_goals_path.exists():
            with open(completed_goals_path, "r") as f:
                contents = f.read().strip()
                return int(contents)
        else:
            return 0

    def __init__(self, parent: qt.QWidget):
        super().__init__(parent)

        self.db = get_db()

        self.unlock_commentary_button = qt.QPushButton()
        self.unlock_commentary_button.setText("Climate Commentary\n(1 goal)")
        self.unlock_commentary_button.clicked.connect(self.on_unlock("commentary"))

        self.unlock_rankings_button = qt.QPushButton()
        self.unlock_rankings_button.setText("Rankings Minigame\n(2 goals)")
        self.unlock_rankings_button.clicked.connect(self.on_unlock("rankings"))

        self.unlock_hangman_button = qt.QPushButton()
        self.unlock_hangman_button.setText("Hangman\n(4 goals)")
        self.unlock_hangman_button.clicked.connect(self.on_unlock("hangman"))

        self.unlock_treefinder_button = qt.QPushButton()
        self.unlock_treefinder_button.setText("Treefinder\n(8 goals)")
        self.unlock_treefinder_button.clicked.connect(self.on_unlock("treefinder"))

        completed_goals = UnlocksWindow.completed_goals()

        self.goals_label = qt.QLabel(f"Goals completed: {completed_goals}")

        if completed_goals < 1:
            self.unlock_commentary_button.setEnabled(False)
        if completed_goals < 2:
            self.unlock_rankings_button.setEnabled(False)
        if completed_goals < 4:
            self.unlock_hangman_button.setEnabled(False)
        if completed_goals < 8:
            self.unlock_treefinder_button.setEnabled(False)

        self.layout = qt.QGridLayout()
        self.layout.setRowStretch(0, 2)
        self.layout.setRowStretch(1, 2)

        self.layout.addWidget(self.unlock_commentary_button, 0, 0)
        self.layout.addWidget(self.unlock_rankings_button, 0, 1)
        self.layout.addWidget(self.unlock_hangman_button, 1, 0)
        self.layout.addWidget(self.unlock_treefinder_button, 1, 1)

        self.main_layout = qt.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.goals_label)
        self.main_layout.addLayout(self.layout)

        self.setLayout(self.main_layout)

        self.setWindowTitle("Unlock Minigames")

    def on_unlock(self, name):
        """
        Callback that activates when the user clicks a button that unlocks a
        minigame.

        :param name: The name of the minigame, according to the database
        :return: A callback function that unlocks a certain minigame
        """
        def inner():
            unlock = self.db.get_unlock_by_name(name)
            unlock.is_unlocked = True

            qt.QMessageBox.about(
                self,
                "Success!",
                f"You have unlocked the '{name}' minigame."
                f" Type '>{'climate_commentary' if name == 'commentary' else name}'"
                f" in the Discord bot to try it out!"
            )

            unlock.update()

        return inner
