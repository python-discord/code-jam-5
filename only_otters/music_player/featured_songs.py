from pathlib import Path
import os
import yaml

__folder__ = Path(__file__).parent

from PyQt5 import QtWidgets, QtGui, QtCore

from .album_button import AlbumButton


def ensure_field(dictlike, fieldname):
    """Ensure the required field is found in the data structure."""
    sentinel = object()
    value = dictlike.get(fieldname, sentinel)

    if value is sentinel:
        raise UserWarning('{!r} is a required field'.format(fieldname))

    return value


class FeaturedSongs(QtWidgets.QFrame):

    chosen_song = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName('featured_songs')
        self.init_ui()
        self.load_songs()
    
    def load_songs(self):
        """Load songs from config file."""
        images_path = Path('only_otters/images').absolute()
        songs_path = Path('only_otters/audio_files').absolute()
        songs_config_file = __folder__ / 'featured_songs.yml'

        yaml_data = yaml.safe_load(open(songs_config_file))

        songs = ensure_field(yaml_data, 'songs')

        for song in songs:
            self.add_featured_song(images_path / ensure_field(song, 'img'), 
                                   songs_path / ensure_field(song, 'audio'))

    def init_ui(self):
        self.setStyleSheet('background: #6F4E37; border-radius: 6px;')
        self.setFixedHeight(190)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(16, 16, 16, 16)
        self.main_layout.setSpacing(3)

        title_font = QtGui.QFont('Raleway', 16)
        title_font.setBold(True)
        self.featured_songs_title = QtWidgets.QLabel('Help Save The Planet...')
        self.featured_songs_title.setFont(title_font)
        self.featured_songs_subtitle = QtWidgets.QLabel('Listen to one of these songs to do your part!')
        title_font.setPointSize(9)

        self.featured_songs_subtitle.setFont(title_font)
        self.featured_songs_layout = QtWidgets.QHBoxLayout()
        self.featured_songs_layout.setContentsMargins(0, 15, 0, 15)
        self.featured_songs_layout.setSpacing(15)
        self.featured_songs_layout.setAlignment(QtCore.Qt.AlignLeft)

        self.main_layout.addWidget(self.featured_songs_title)
        self.main_layout.addWidget(self.featured_songs_subtitle)
        self.main_layout.addLayout(self.featured_songs_layout)

        self.setLayout(self.main_layout)
    
    def add_featured_song(self, imgfile: str, audiofile: str):

        imgfile = os.fspath(imgfile)
        audiofile = os.fspath(audiofile)

        featured_song = AlbumButton(imgfile, audiofile)
        featured_song.selected.connect(self.chosen_song.emit)
        self.featured_songs_layout.addWidget(featured_song)