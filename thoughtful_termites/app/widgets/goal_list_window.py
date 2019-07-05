from thoughtful_termites.app import qt

from .goal_list import GoalList
from .add_goal_window import AddGoalWindow

active_goal_windows = set()


class GoalListWindow(qt.QWidget):
    def __init__(self):
        super().__init__()

        self.goal_list = GoalList()

        self.add_goal_button = qt.QPushButton()
        self.add_goal_button.setText('Add Goal')
        self.add_goal_button.clicked.connect(
            self.on_add_goal
        )

        self.main_layout = qt.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addWidget(self.goal_list)
        self.main_layout.addWidget(self.add_goal_button)

        self.setWindowTitle('Goal List')

    def on_add_goal(self):
        add_goal_window = AddGoalWindow()

        def add_goal_callback(window: AddGoalWindow):
            def callback():
                item = qt.QListWidgetItem(
                    window.name_box.text()
                )

                item.setToolTip(
                    window.desc_box.text()
                )

                self.goal_list.addItem(item)
                active_goal_windows.remove(window)
                window.close()
            return callback

        add_goal_window.done_button.clicked.connect(
            add_goal_callback(add_goal_window)
        )
        active_goal_windows.add(add_goal_window)
        add_goal_window.show()
