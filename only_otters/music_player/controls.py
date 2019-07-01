from PyQt5 import QtWidgets, QtMultimedia, QtCore


class ControlsWidget(QtWidgets.QWidget):
    """Contains all the controls for a QMediaPlayer."""

    def __init__(self, player):
        super().__init__()
        self.player = player
        self.init_ui()

    def init_ui(self):
        """Create the UI."""
        self.main_layout = QtWidgets.QHBoxLayout()

        self.previous_song_button = QtWidgets.QPushButton('<<')
        self.previous_song_button.clicked.connect(self._previous_song)
        self.play_pause_button = QtWidgets.QPushButton('Play')
        self.play_pause_button.clicked.connect(self._toggle_play)
        self.next_song_button = QtWidgets.QPushButton('>>')
        self.next_song_button.clicked.connect(self._next_song)
        self.open_file_button = QtWidgets.QPushButton('Open Audio File...')
        self.open_file_button.clicked.connect(self._open_file)

        self.main_layout.addWidget(self.previous_song_button)
        self.main_layout.addWidget(self.play_pause_button)
        self.main_layout.addWidget(self.next_song_button)
        self.main_layout.addWidget(self.open_file_button)

        self.setLayout(self.main_layout)

    def _toggle_play(self):
        """Toggle between play and pause."""
        if self.play_pause_button.text() == 'Play':
            self.play_pause_button.setText('Pause')
            self.player.play()
        else:
            self.play_pause_button.setText('Play')
            self.player.pause()

    def _next_song(self):
        """Plays the next song in the playlist."""
        self.player.playlist().next()
        if self.player.state() == QtMultimedia.QMediaPlayer.PausedState:
            self._toggle_play()

    def _previous_song(self):
        """Plays previous song in the playlist."""
        self.player.playlist().previous()
        if self.player.state() == QtMultimedia.QMediaPlayer.PausedState:
            self._toggle_play()

    def _open_file(self):
        """Opens an audio file and adds it to the playlist."""
        song = QtWidgets.QFileDialog.getOpenFileName(self, "Open Song", "", "Sound Files (*.mp3)")

        if song[0]:
            url = QtCore.QUrl.fromLocalFile(song[0])

            if not self.player.playlist().mediaCount():
                self.player.playlist().addMedia(QtMultimedia.QMediaContent(url))
                self._toggle_play()
            else:
                self.player.playlist().addMedia(QtMultimedia.QMediaContent(url))
