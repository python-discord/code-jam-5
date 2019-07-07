import sys

from thoughtful_termites.shared import qt
from ..controlled_processes import (
    ControlledProcess,
    BotControlledProcess,
    GoalsProcess,
)

from thoughtful_termites.shared.resources import leaf_icon_path


class ControlPanel(qt.QWidget):
    def __init__(self):
        super().__init__()

        self.bot_process = BotControlledProcess()
        self.goals_process = ControlledProcess(GoalsProcess)

        self.configure_bot_button = qt.QPushButton('Configure Bot')
        self.configure_bot_button.clicked.connect(
            self.on_configure_bot
        )

        self.run_bot_button = qt.QPushButton('Start Bot')
        self.run_bot_button.clicked.connect(self.bot_process.toggle)

        self.open_goals_button = qt.QPushButton('Open Goals')
        self.open_goals_button.clicked.connect(self.goals_process.toggle)

        self.goals_process.started.connect(
            lambda: self.open_goals_button.setText('Close Goals')
        )

        self.goals_process.finished.connect(
            lambda: self.open_goals_button.setText('Open Goals')
        )

        self.system_tray_icon = qt.QSystemTrayIcon()
        self.system_tray_icon.setToolTip('Climate Bot')
        self.system_tray_icon.setIcon(qt.QIcon(str(leaf_icon_path)))
        self.system_tray_icon.setVisible(True)
        self.system_tray_icon.activated.connect(
            self.on_tray_icon_activation
        )

        self.system_tray_context_menu = qt.QMenu()
        self.system_tray_context_menu.addAction(
            'Climate Bot Control Panel',
        ).setDisabled(True)

        self.system_tray_context_menu.addSeparator()
        self.system_tray_context_menu.addAction(
            'Show', self.super_show
        )

        self.system_tray_context_menu.addAction(
            'Exit', sys.exit
        )

        self.system_tray_icon.setContextMenu(
            self.system_tray_context_menu
        )

        self.main_layout = qt.QVBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.configure_bot_button)
        self.main_layout.addWidget(self.run_bot_button)
        self.main_layout.addWidget(self.open_goals_button)

        self.setMaximumHeight(0)
        self.setFixedWidth(360)
        self.setWindowTitle('Climate Bot')

    def event(self, event: qt.QEvent) -> bool:
        if event.type() == qt.QEvent.WindowStateChange:
            if self.isMinimized():
                self.hide()
                self.system_tray_icon.showMessage(
                    'Climate Bot',
                    'Minimized to system tray.',
                )
                event.ignore()
            else:
                event.accept()
        return super().event(event)

    def super_show(self):
        self.setWindowState(
            self.windowState() &
            ~qt.constants.WindowMinimized |
            qt.constants.WindowActive
        )
        self.show()
        self.raise_()
        self.activateWindow()

    def on_tray_icon_activation(self, reason):
        if reason == self.system_tray_icon.DoubleClick:
            if self.isVisible() and not self.isMinimized():
                self.hide()
            else:
                self.super_show()

        elif reason == self.system_tray_icon.Context:
            pass

    def on_configure_bot(self):
        from thoughtful_termites.shared.bot_config import Config
        from thoughtful_termites.shared.constants import config_path

        config = Config.load(config_path)

        bot_token, ok = qt.QInputDialog.getText(
            self, 'Bot Token', 'Enter bot token',
            qt.QLineEdit.Normal, config.bot_token
        )

        if ok:
            config.bot_token = bot_token

        client_id, ok = qt.QInputDialog.getText(
            self, 'Client ID', 'Enter client ID',
            qt.QLineEdit.Normal, config.client_id
        )

        if ok:
            config.client_id = client_id

        while True:
            owner_id, ok = qt.QInputDialog.getText(
                self, 'Owner ID', 'Enter owner ID',
                qt.QLineEdit.Normal, str(config.owner_id)
            )

            if ok:
                try:
                    config.owner_id = int(owner_id)
                    break

                except ValueError:
                    pass
            else:
                break

        config.save(config_path)

    # def closeEvent(self, event: qt.QCloseEvent) -> None:
    #     event.ignore()
    #     self.hide()
