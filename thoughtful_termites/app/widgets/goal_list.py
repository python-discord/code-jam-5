from thoughtful_termites.app import qt
from .reminder_list_window import ReminderListWindow


class GoalListItem(qt.QListWidgetItem):
    def __init__(self):
        super().__init__()


class GoalList(qt.QListWidget):
    def __init__(self):
        super().__init__()

        self.setContextMenuPolicy(qt.constants.CustomContextMenu)
        self.customContextMenuRequested.connect(
            self.on_context_menu
        )

        self.setSelectionMode(self.ExtendedSelection)

    def on_context_menu(self, pos: qt.QPoint):
        item = self.itemAt(pos)
        selected_items = self.selectedItems()

        def edit_reminders_callback(item):
            def callback():
                edit_reminder_window = ReminderListWindow(self.window())
                edit_reminder_window.show()

            return callback

        # def edit_goal_callback(item):
        #     def callback():


        if item:
            menu = qt.QMenu()
            menu.addAction('Edit Goal')
            menu.addAction('Edit Reminders', edit_reminders_callback(item))
            menu.addAction('Delete')

            menu.exec(self.mapToGlobal(pos))


