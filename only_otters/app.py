from PyQt5 import QtWidgets, QtGui
from .music_player import MusicPlayer
from only_otters.images import icons

class Leafify(QtWidgets.QMainWindow):
    """A music player designed to encourage action against climate change."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Leafify')
        self.setWindowIcon(QtGui.QIcon(icons.Logo.str))
        self.setMinimumSize(950, 650)
        self.init_gui()

    def init_gui(self):
        """Initialises the GUI."""
        self.main_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.music_player = MusicPlayer()

        self.main_layout.addWidget(self.music_player)
        self.main_widget.setLayout(self.main_layout)
