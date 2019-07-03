from PyQt5 import QtWidgets, QtGui, QtCore
from .album_button import AlbumButton
from pathlib import Path


class FeaturedSongs(QtWidgets.QFrame):

    chosen_song = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName('featured_songs')
        self.init_ui()

        images_path = Path('only_otters/images')
        songs_path = Path('only_otters/audio_files')

        self.add_featured_song(str(images_path / 'earth_cover.png'),
                               str(songs_path / 'Lil Dicky - Earth.mp3'))
        self.add_featured_song(str(images_path / 'wonderful_world_cover.jpg'),
                               str(songs_path / 'Louis Armstrong - What a Wonderful World.mp3'))
        self.add_featured_song(str(images_path / 'earth_song_cover.jpg'),
                               str(songs_path / 'Michael Jackson - Earth Song.mp3'))
        self.add_featured_song(str(images_path / 'heal_world_cover.png'),
                               str(songs_path / 'Michael Jackson - Heal The World.mp3'))
        self.add_featured_song(str(images_path / 'lovesong_cover.jpg'),
                               str(songs_path / 'Paul McCartney - Love Song To The Earth.mp3'))
    
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
    
    def add_featured_song(self, text, image):
        featured_song = AlbumButton(text, image)
        featured_song.selected.connect(self.chosen_song.emit)
        self.featured_songs_layout.addWidget(featured_song)