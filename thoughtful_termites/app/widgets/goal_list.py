from thoughtful_termites.shared import qt
from .reminder_list_window import ReminderListWindow
from .edit_goal_window import EditGoalWindow

from thoughtful_termites.shared.goal_db import GoalDB


class GoalListItem(qt.QListWidgetItem):
    def __init__(self, goal):
        super().__init__()

        self.goal = goal
        self.setText(goal.name)


class GoalList(qt.QListWidget):
    def __init__(self, db: GoalDB):
        super().__init__()

        self.db = db

        self.setContextMenuPolicy(qt.constants.CustomContextMenu)
        self.customContextMenuRequested.connect(
            self.on_context_menu
        )

        self.setSelectionMode(self.ExtendedSelection)

    def on_context_menu(self, pos: qt.QPoint):
        item: GoalListItem = self.itemAt(pos)
        selected_items = self.selectedItems()

        def on_edit_reminders():
            edit_reminder_window = ReminderListWindow(
                self.window(),
                item.goal,
            )
            edit_reminder_window.exec()

        def on_edit_goal():
            edit_goal_window = EditGoalWindow(self.window())
            edit_goal_window.name_box.setText(item.goal.name)
            edit_goal_window.desc_box.setText(item.goal.desc)

            def on_done():
                item.goal.name = edit_goal_window.name_box.text()
                item.goal.desc = edit_goal_window.desc_box.text()

                item.goal.update()
                item.setText(item.goal.name)

                edit_goal_window.done(0)

            edit_goal_window.done_button.clicked.connect(
                on_done
            )

            edit_goal_window.exec()

        def on_delete():
            for item in selected_items:  # type: GoalListItem
                item.goal.delete()
                self.takeItem(self.row(item))

        # def edit_goal_callback(item):
        #     def callback():

        if item:
            menu = qt.QMenu()
            menu.addAction('Edit Goal', on_edit_goal)
            menu.addAction('Edit Reminders', on_edit_reminders)
            menu.addAction('Delete', on_delete)

            menu.exec(self.mapToGlobal(pos))
