from PyQt5 import QtWidgets, QtCore


class MusicPlayer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Music Player')
        self.resize(1280, 720)

        label = QtWidgets.QLabel('Hello World')
        label.setAlignment(QtCore.Qt.AlignCenter)

        self.setCentralWidget(label)

#testing git
