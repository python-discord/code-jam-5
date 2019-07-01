from PyQt5 import QtWidgets, QtMultimedia, QtGui, QtCore
from .controls import ControlsWidget
from .now_playing import NowPlayingWidget
from pathlib import Path


class MusicPlayer(QtWidgets.QWidget):
    """Represents a MusicPlayer object, for playing/pausing/loading music."""

    def __init__(self):
        super().__init__()
        self.player = QtMultimedia.QMediaPlayer()
        self.playlist = QtMultimedia.QMediaPlaylist()
        self.player.setPlaylist(self.playlist)

        self.init_ui()

    def init_ui(self):
        """Create the UI."""
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.vertical_spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Fixed,
                                                     QtWidgets.QSizePolicy.Expanding)

        self.now_playing_widget = NowPlayingWidget(self.player)

        images_path = Path('only_otters/images')
        self.moon_foreground_image = QtGui.QPixmap(str(images_path / 'moon_foreground.png'))
        self.moon_foreground_label = QtWidgets.QLabel(self)
        self.moon_foreground_label.setPixmap(self.moon_foreground_image)

        self.contents_widget = QtWidgets.QFrame()
        self.contents_widget.setStyleSheet('background: #d8d8d8;')
        self.contents_widget.setSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Expanding)

        self.controls = ControlsWidget(self.player)

        self.main_layout.addWidget(self.now_playing_widget)
        self.main_layout.addWidget(self.contents_widget)
        self.main_layout.addWidget(self.controls)

        self.setLayout(self.main_layout)

    def resizeEvent(self, event):
        """Handles the positioning and sizing of the moon foreground image."""
        scaled = self.moon_foreground_image.scaled(max(self.width(), 1920), 99999999,
                                                   QtCore.Qt.KeepAspectRatio)
        self.moon_foreground_label.setPixmap(scaled)

        self.moon_foreground_label.move(0, self.now_playing_widget.y() +
                                        self.now_playing_widget.height() - scaled.height()*0.65)
        self.moon_foreground_label.resize(self.width(), scaled.height())
        self.moon_foreground_label.raise_()
