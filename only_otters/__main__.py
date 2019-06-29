from app import MusicPlayer
from PyQt5 import QtWidgets
import sys


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = MusicPlayer()
    sys.exit(app.exec_())
