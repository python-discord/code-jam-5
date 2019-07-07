# local
from ..audio_visualiser import AudioVisualiser

# std
from pathlib import Path

# qt
from PyQt5 import QtWidgets, QtGui, QtCore, QtMultimedia


class NowPlayingWidget(QtWidgets.QFrame):
    """Shows the music as it plays from a QMediaPlayer"""

    def __init__(self, player: 'MusicPlayer'):
        super().__init__()
        self.player = player
        self.player.playlist().currentMediaChanged.connect(self._media_changed)
        self.setObjectName('now_playing')
        self.setMaximumHeight(218)
        self.init_ui()

    def init_ui(self):

        background_file = Path('only_otters/images/background.png')
        self.background_pixmap = QtGui.QPixmap(str(background_file))
        self.background_label = QtWidgets.QLabel(self)

        self.main_layout = QtWidgets.QHBoxLayout()

        self.audio_visualiser = AudioVisualiser(self.player)

        now_playing_font = QtGui.QFont('Raleway', 24)
        self.now_playing_label = QtWidgets.QLabel('Not Playing Anything')
        self.now_playing_label.setStyleSheet('color: white;')
        self.now_playing_label.setFont(now_playing_font)

        self.main_layout.addWidget(self.audio_visualiser)
        self.main_layout.addWidget(self.now_playing_label)
        self.setLayout(self.main_layout)

    def _media_changed(self, media: QtMultimedia.QMediaContent):
        """Update 'Now playing' label when a new song is selected."""
        filename = media.canonicalUrl().fileName()
        song_name = '.'.join(filename.split('.')[:-1])
        self.now_playing_label.setText(song_name)

    def adjust_background(self):
        """Adjusts the background to make it fit."""
        self.background_label.resize(self.width(), self.height())
        self.background_label.setPixmap(self.background_pixmap.scaled(
            self.width(), self.height(), QtCore.Qt.KeepAspectRatioByExpanding))

    def resizeEvent(self, event):
        self.adjust_background()
