from PyQt5 import QtWidgets, QtGui


class VisualiserWidget(QtWidgets.QWidget):
    """Visualises the music as it plays from a QMediaPlayer"""

    def __init__(self, player):
        super().__init__()
        self.player = player
        self.player.playlist().currentMediaChanged.connect(self._media_changed)

        self.init_ui()

    def init_ui(self):
        self.main_layout = QtWidgets.QHBoxLayout()

        now_playing_font = QtGui.QFont('Calibri', 16)
        self.now_playing_label = QtWidgets.QLabel('Now Playing: N/A')
        self.now_playing_label.setFont(now_playing_font)

        self.main_layout.addWidget(self.now_playing_label)
        self.setLayout(self.main_layout)

    def _media_changed(self, media):
        self.now_playing_label.setText(f'Now Playing: {media.canonicalUrl().fileName()}')
