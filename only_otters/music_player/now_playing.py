from PyQt5 import QtWidgets, QtGui, QtCore
from ..audio_visualiser import AudioVisualiser
from pathlib import Path


class NowPlayingWidget(QtWidgets.QFrame):
    """Shows the music as it plays from a QMediaPlayer"""

    def __init__(self, player):
        super().__init__()
        self.player = player
        self.player.playlist().currentMediaChanged.connect(self._media_changed)
        self.setObjectName('now_playing')
        self.setMaximumHeight(218)
        self.init_ui()

    def init_ui(self):
        background_file = Path('only_otters/images/background.jpeg')
        self.background_pixmap = QtGui.QPixmap(str(background_file))
        self.background_label = QtWidgets.QLabel(self)

        self.main_layout = QtWidgets.QHBoxLayout()

        self.audio_visualiser = AudioVisualiser(self.player)

        now_playing_font = QtGui.QFont('Raleway', 24)
        self.now_playing_label = QtWidgets.QLabel('Now Playing: N/A')
        self.now_playing_label.setStyleSheet('color: white;')
        self.now_playing_label.setFont(now_playing_font)

        self.main_layout.addWidget(self.audio_visualiser)
        self.main_layout.addWidget(self.now_playing_label)
        self.setLayout(self.main_layout)

    def _media_changed(self, media):
        self.now_playing_label.setText(f'Now Playing: {media.canonicalUrl().fileName()}')

    def adjust_background(self):
        """Adjusts the background to make it fit"""
        self.background_label.resize(self.width(), self.height())
        self.background_label.setPixmap(self.background_pixmap.scaled(
            self.width(), self.height(), QtCore.Qt.KeepAspectRatioByExpanding))

    def resizeEvent(self, event):
        self.adjust_background()