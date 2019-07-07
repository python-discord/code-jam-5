from .app import Leafify
from PyQt5 import QtWidgets, QtGui
from pathlib import Path
import sys


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    font_path = Path('only_otters/fonts')
    QtGui.QFontDatabase.addApplicationFont(str(font_path / 'Raleway-Regular.ttf'))
    QtGui.QFontDatabase.addApplicationFont(str(font_path / 'Raleway-SemiBold.ttf'))

    gui = Leafify()
    gui.show()
    sys.exit(app.exec_())
