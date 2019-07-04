from PyQt5 import QtWidgets, QtMultimedia, QtGui, QtCore
from .controls import ControlsWidget
from .now_playing import NowPlayingWidget
from .featured_songs import FeaturedSongs
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
        self.setStyleSheet('QLabel { color: white; }')

        self.vertical_spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Fixed,
                                                     QtWidgets.QSizePolicy.Expanding)

        self.now_playing_widget = NowPlayingWidget(self.player)

        images_path = Path('only_otters/images')
        self.foreground_image = QtGui.QPixmap(str(images_path / 'foreground.png'))
        self.foreground_label = QtWidgets.QLabel(self)
        self.foreground_label.setPixmap(self.foreground_image)

        self.contents_widget = QtWidgets.QFrame()
        self.contents_widget.setStyleSheet('background: qlineargradient(spread:pad, '
                                           'x1:0.495, y1:0, x2:0.5, y2:1,'
                                           'stop:0 rgba(155, 118, 83, 255),'
                                           'stop:1 rgba(122, 93, 65, 255))')
        self.contents_widget.setSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Expanding)
        self.contents_layout = QtWidgets.QHBoxLayout()
        self.contents_layout.setContentsMargins(50, 60, 50, 50)
        self.main_content_layout = QtWidgets.QVBoxLayout()
        self.main_content_layout.setAlignment(QtCore.Qt.AlignLeft)
        self.sidebar_layout = QtWidgets.QVBoxLayout()

        self.featured_songs = FeaturedSongs()
        self.featured_songs.chosen_song.connect(self.play_song)
        self.featured_songs.chosen_song.connect(
            self.now_playing_widget.audio_visualiser.green_flames)

        self.open_file_button = QtWidgets.QPushButton('Open File to Play')
        self.open_file_button.clicked.connect(self.open_file)

        self.main_content_layout.addWidget(self.featured_songs)
        self.main_content_layout.addWidget(self.open_file_button)
        self.main_content_layout.addItem(self.vertical_spacer)

        self.contents_layout.addLayout(self.main_content_layout)
        self.contents_layout.addLayout(self.sidebar_layout)
        self.contents_widget.setLayout(self.contents_layout)

        self.controls = ControlsWidget(self.player)

        self.main_layout.addWidget(self.now_playing_widget)
        self.main_layout.addWidget(self.contents_widget)
        self.main_layout.addWidget(self.controls)

        self.setLayout(self.main_layout)

    def open_file(self):
        song = QtWidgets.QFileDialog.getOpenFileName(self, "Open Song", "", "Sound Files (*.mp3)")
        if song:
            self.now_playing_widget.audio_visualiser.red_flames()
            self.play_song(song[0])

    def play_song(self, song):
        self.controls.duration_label.setText('Loading...')
        url = QtCore.QUrl.fromLocalFile(song)
        self.player.playlist().insertMedia(self.player.playlist().nextIndex(),
                                           QtMultimedia.QMediaContent(url))
        if self.player.playlist().mediaCount() == 1:
            self.controls.toggle_play()
        else:
            self.controls._next_song()
        self.controls.duration_label.setText('0')

    def resizeEvent(self, event):
        """Handles the positioning and sizing of the moon foreground image."""
        scaled = self.foreground_image.scaled(max(self.width(), 1920), 99999999,
                                              QtCore.Qt.KeepAspectRatio)
        self.foreground_label.setPixmap(scaled)

        self.foreground_label.move(0, self.now_playing_widget.y() +
                                   self.now_playing_widget.height() - scaled.height()*0.65)
        self.foreground_label.resize(self.width(), scaled.height())
        self.foreground_label.raise_()
