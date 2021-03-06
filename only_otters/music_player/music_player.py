# local
from .controls import ControlsWidget
from .media_library import MediaLibrary
from .now_playing import NowPlayingWidget
from only_otters.facts import get_fact_by_tags
from only_otters.facts.audio import text_to_audio
from only_otters.images import buttons as imgButtons

# std
from pathlib import Path

# qt
from PyQt5 import QtWidgets, QtMultimedia, QtGui, QtCore


class MusicPlayer(QtWidgets.QWidget):
    """Represents a MusicPlayer object, for playing/pausing/loading music."""

    # Every {} songs, an ad will be played automatically
    total_songs_between_adverts: int = 1

    fact_refresh_rate = 8

    def __init__(self):
        super().__init__()
        self.player = QtMultimedia.QMediaPlayer()
        self.playlist = QtMultimedia.QMediaPlaylist()
        self.player.setPlaylist(self.playlist)
        self.player.playlist().currentMediaChanged.connect(self.disable_advert_controls)
        self.advert_in_progress = False

        self.advert_counter = self.total_songs_between_adverts - 1

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
        self.contents_layout.setSpacing(30)
        self.main_content_layout = QtWidgets.QVBoxLayout()
        self.main_content_layout.setAlignment(QtCore.Qt.AlignLeft)
        self.sidebar_layout = QtWidgets.QVBoxLayout()
        self.sidebar_layout.setSpacing(0)

        self.media_library = MediaLibrary()
        self.media_library.song_triggered.connect(self.play_song)

        self.main_content_layout.addWidget(self.media_library)
        self.main_content_layout.addItem(self.vertical_spacer)

        self.fact_title_frame = QtWidgets.QFrame()
        self.fact_title_frame.setStyleSheet('background: #57bd4f;'
                                            'border-top-left-radius: 6px;'
                                            'border-top-right-radius: 6px;'
                                            'color: white;')
        self.fact_title_layout = QtWidgets.QHBoxLayout()
        title_font = QtGui.QFont('Raleway', 16)
        title_font.setBold(True)
        self.fact_title_label = QtWidgets.QLabel('Climate Change Facts')
        self.fact_title_label.setFont(title_font)
        self.fact_title_layout.addWidget(self.fact_title_label)
        self.fact_title_frame.setLayout(self.fact_title_layout)

        self.fact_widget = get_fact_by_tags('ui').as_widget(self)
        self.fact_widget.setMinimumSize(300, 200)

        self.next_fact_button = QtWidgets.QPushButton("Next Fact", self)
        self.next_fact_button.clicked.connect(self.refresh_fact)
        self.next_fact_button.setStyleSheet('background: #78543b;'
                                            'padding: 7px;'
                                            'border-bottom-left-radius: 6px;'
                                            'border-bottom-right-radius: 6px;'
                                            'color: white;')

        self.refresh_fact_timer = QtCore.QTimer(self)
        self.refresh_fact_timer.timeout.connect(self.refresh_fact)
        self.refresh_fact_timer.start(self.fact_refresh_rate * 1000)

        self.sidebar_layout.addWidget(self.fact_title_frame)
        self.sidebar_layout.addWidget(self.fact_widget)
        self.sidebar_layout.addWidget(self.next_fact_button)
        self.sidebar_layout.addItem(self.vertical_spacer)

        self.contents_layout.addLayout(self.main_content_layout)
        self.contents_layout.addLayout(self.sidebar_layout)
        self.contents_widget.setLayout(self.contents_layout)

        self.controls = ControlsWidget(self.player)

        self.main_layout.addWidget(self.now_playing_widget)
        self.main_layout.addWidget(self.contents_widget)
        self.main_layout.addWidget(self.controls)

        self.setLayout(self.main_layout)

    def play_song(self, song: str):
        """Play a song given its file url in the local filesystem."""
        self.player.playlist().clear()
        self.controls.duration_label.setText('Loading...')
        url = QtCore.QUrl.fromLocalFile(song)

        if self.check_advert_intermission():
            self.player.playlist().addMedia(QtMultimedia.QMediaContent(url))
        else:
            self.player.playlist().insertMedia(
                self.player.playlist().nextIndex(),
                QtMultimedia.QMediaContent(url)
            )

            if self.player.playlist().mediaCount() == 1:
                self.controls.toggle_play()
            else:
                self.controls._next_song()
        self.controls.duration_label.setText('0')
        self.controls.play_pause_button.setIcon(QtGui.QIcon(imgButtons.Pause.str))

    def disable_advert_controls(self, media: QtMultimedia.QMediaContent):
        """Disable player controls while an ad is playing."""
        if self.advert_in_progress:
            self.now_playing_widget.audio_visualiser.green_flames()
            self.controls.setEnabled(False)
            self.advert_in_progress = False
        else:
            self.now_playing_widget.audio_visualiser.red_flames()
            self.controls.setEnabled(True)

    def play_ad(self):
        """Play an ad before a song is played."""
        self.advert_in_progress = True

        fact = get_fact_by_tags('text')
        text = "Did you know that ... " + fact.content + '. Thank you for listening to Leafify'

        file = text_to_audio(text)
        self.play_song(file)

        self.now_playing_widget.now_playing_label.setText('Advert Intermission')

    def check_advert_intermission(self):
        """
        Callback for every time the media player's status changes.
        Will play an ad after each song. 'ADVERT' is a on/off
        """
        if not self.advert_counter:
            self.advert_counter = self.total_songs_between_adverts
            self.play_ad()
            return True
        else:
            self.advert_counter -= 1
            return False

    def resizeEvent(self, event):
        """Handles the positioning and sizing of the moon foreground image."""
        scaled = self.foreground_image.scaled(max(self.width(), 1920), 99999999,
                                              QtCore.Qt.KeepAspectRatio)
        self.foreground_label.setPixmap(scaled)

        self.foreground_label.move(0, self.now_playing_widget.y() +
                                   self.now_playing_widget.height() - scaled.height()*0.65)
        self.foreground_label.resize(self.width(), scaled.height())
        self.foreground_label.raise_()

    def refresh_fact(self):
        """Refresh the fact widget."""

        # Delete previous widget
        self.fact_widget.deleteLater()

        # Prepare widget
        self.fact_widget = get_fact_by_tags('ui').as_widget(self)
        self.fact_widget.setMinimumSize(300, 200)

        # Place widget
        self.sidebar_layout.insertWidget(1, self.fact_widget)

        # Reset timer
        self.refresh_fact_timer.start(self.fact_refresh_rate * 1000)
