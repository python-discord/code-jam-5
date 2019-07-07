from PyQt5 import QtWidgets, QtMultimedia, QtGui
from .seeker import Seeker
from pathlib import Path

from only_otters.images import buttons as imgButtons
from only_otters.ads.tts import as_callack_audio


class ControlsWidget(QtWidgets.QFrame):
    """Contains all the controls for a QMediaPlayer."""

    def __init__(self, player):
        super().__init__()
        self.player = player
        self.player.mediaStatusChanged.connect(self._update_controls_on_stop)
        self.player.playlist().currentMediaChanged.connect(self._update_play_pause_button)
        self.setObjectName('controls')
        self.setFixedHeight(50)
        self.init_ui()


    def init_ui(self):
        """Create the UI."""
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setContentsMargins(6, 6, 6, 6)
        self.setStyleSheet('QFrame#controls { background: qlineargradient(spread:pad, x1:0.494682, y1:0, x2:0.5, y2:1,'
                           'stop:0 rgba(136, 140, 141, 255), stop:1 rgba(113, 116, 117, 255)); }'
                           'QPushButton { border: none; background: none; color: white; }')

        self.seeker = Seeker(self.player)

        self.previous_song_icon = QtGui.QIcon(imgButtons.Previous.str)
        self.pause_song_icon = QtGui.QIcon(imgButtons.Pause.str)
        self.play_song_icon = QtGui.QIcon(imgButtons.Play.str)
        self.next_song_icon = QtGui.QIcon(imgButtons.Next.str)

        self.previous_song_button = QtWidgets.QPushButton(self.previous_song_icon, '')
        # self.previous_song_button.setStyleSheet("background:none")
        self.previous_song_button.clicked.connect(self._previous_song)
        self.play_pause_button = QtWidgets.QPushButton(self.play_song_icon, '')
        self.play_pause_button.clicked.connect(self.toggle_play)
        self.next_song_button = QtWidgets.QPushButton(self.next_song_icon, '')
        self.next_song_button.clicked.connect(self._next_song)
        self.duration_label = QtWidgets.QLabel('00:00')
        self.duration_label.setFont(QtGui.QFont('Raleway'))
        self.seeker.timestamp_updated.connect(self.duration_label.setText)

        self.main_layout.addWidget(self.previous_song_button)
        self.main_layout.addWidget(self.play_pause_button)
        self.main_layout.addWidget(self.next_song_button)
        self.main_layout.addWidget(self.seeker)
        self.main_layout.addWidget(self.duration_label)

        self.setLayout(self.main_layout)

    def _update_controls_on_stop(self, status):
        if status == self.player.EndOfMedia:
            self.play_pause_button.setIcon(self.play_song_icon)
            self.seeker.setValue(0)
        
    def _update_play_pause_button(self, state):
        if self.player.state() == self.player.PlayingState:
            self.play_pause_button.setIcon(self.pause_song_icon)
        else:
            self.play_pause_button.setIcon(self.play_song_icon)

    def toggle_play(self):
        """Toggle between play and pause."""
        if self.player.state() == self.player.PlayingState:
            self.player.pause()
            self.play_pause_button.setIcon(self.play_song_icon)
        elif self.player.playlist().mediaCount():
            self.player.play()
            self.play_pause_button.setIcon(self.pause_song_icon)

    def _next_song(self):
        """Plays the next song in the playlist."""
        self.player.playlist().next()
        self.player.play()
        if self.player.state() == QtMultimedia.QMediaPlayer.PausedState:
            self.toggle_play()

    def _previous_song(self):
        """Plays previous song in the playlist."""
        self.player.playlist().previous()
        if self.player.state() == QtMultimedia.QMediaPlayer.PausedState:
            self.toggle_play()

    def _open_file(self):
        """Opens an audio file and adds it to the playlist."""
        song = QtWidgets.QFileDialog.getOpenFileName(self, "Open Song", "", "Sound Files (*.mp3)")

        if song[0]:
            url = QtCore.QUrl.fromLocalFile(song[0])

            if not self.player.playlist().mediaCount():
                self.player.playlist().addMedia(QtMultimedia.QMediaContent(url))
                self.toggle_play()
            else:
                self.player.playlist().addMedia(QtMultimedia.QMediaContent(url))
