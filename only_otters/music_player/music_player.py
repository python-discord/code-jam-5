from PyQt5 import QtWidgets, QtMultimedia
from .controls import ControlsWidget
from .visualiser import NowPlayingWidget


class MusicPlayer(QtWidgets.QWidget):
    """Represents a MusicPlayer object, for playing/pausing/loading music"""

    def __init__(self):
        super().__init__()
        self.player = QtMultimedia.QMediaPlayer()
        self.playlist = QtMultimedia.QMediaPlaylist()
        self.player.setPlaylist(self.playlist)

        self.init_ui()

    def init_ui(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)

        self.visualiser = NowPlayingWidget(self.player)
        self.main_layout.addWidget(self.visualiser)

        self.controls = ControlsWidget(self.player)
        self.main_layout.addWidget(self.controls)

        self.setLayout(self.main_layout)
