from thoughtful_termites.app import qt


class ReminderListItem(qt.QListWidgetItem):
    def __init__(self):
        super().__init__()


class ReminderList(qt.QListWidget):
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

        if item:
            menu = qt.QMenu()
            menu.addAction('Edit')
            menu.addAction('Delete')

            menu.exec(self.mapToGlobal(pos))
