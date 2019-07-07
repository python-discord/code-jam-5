from pathlib import Path
from PyQt5 import QtWidgets, QtCore, QtGui
import os


__folder__ = Path(__file__).parent


def find_user_library():
    expected_path = Path('~/Music').expanduser()
    if expected_path.exists():
        return expected_path


class MediaLibrary(QtWidgets.QFrame):

    song_triggered = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()

        ep = find_user_library()
        if ep is not None:
            self.set_path(ep)
    
    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        self.title_frame = QtWidgets.QFrame()
        self.title_frame.setStyleSheet('background: #57bd4f;'
                                       'border-top-left-radius: 6px;'
                                       'border-top-right-radius: 6px;'
                                       'color: white;')
        self.title_layout = QtWidgets.QHBoxLayout()
        self.title_frame.setLayout(self.title_layout)
        self.layout().addWidget(self.title_frame)

        self.library_frame = QtWidgets.QFrame()
        self.library_frame.setStyleSheet('background: #78543b;'
                                         'border-bottom-left-radius: 6px;'
                                         'border-bottom-right-radius: 6px;'
                                         'color: white;')
        self.library_layout = QtWidgets.QVBoxLayout()
        self.library_frame.setLayout(self.library_layout)
        self.layout().addWidget(self.library_frame)

        title_font = QtGui.QFont('Raleway', 16)
        title_font.setBold(True)
        self.media_library_title = QtWidgets.QLabel('Media Library...')
        self.media_library_title.setFont(title_font)
        self.title_layout.addWidget(self.media_library_title)

        self.filesystem_model = QtWidgets.QFileSystemModel()
        self.filesystem_model.setNameFilters(['*.mp3', '*.m4a', '*.wav', '*.m3u', '*.ogg', '*.wma'])
        self.filesystem_model.setNameFilterDisables(False)
        self.filesystem_model.setFilter(QtCore.QDir.AllEntries | QtCore.QDir.NoDotAndDotDot)
        self.music_tree = QtWidgets.QTreeView(self)
        self.music_tree.setModel(self.filesystem_model)
        self.music_tree.hideColumn(1) # Size Column
        self.music_tree.hideColumn(2) # Type Column
        self.music_tree.hideColumn(3) # Date Modified Column
        self.music_tree.setObjectName('music_library')
        self.music_tree.setHeaderHidden(True)
        self.music_tree.activated.connect(self.item_clicked)
        self.library_layout.addWidget(self.music_tree)

        self.change_path_button = QtWidgets.QPushButton('Change Path')
        self.library_layout.addWidget(self.change_path_button)
        self.change_path_button.clicked.connect(self.choose_path)

    def choose_path(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory()
        if folder_path:
            self.set_path(str(Path(folder_path)))

    def set_path(self, path):
        path = os.fspath(path)
        x = self.filesystem_model.setRootPath(path)
        self.music_tree.setRootIndex(x)
    
    def item_clicked(self, index):
        path = str(self.filesystem_model.filePath(index))
        if os.path.isfile(path):
            self.song_triggered.emit(path)