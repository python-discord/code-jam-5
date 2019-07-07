from .app import Leafify
from PyQt5 import QtWidgets, QtGui
from pathlib import Path
import sys

from .fonts import Raleway


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    QtGui.QFontDatabase.addApplicationFont(Raleway.Regular.str)
    QtGui.QFontDatabase.addApplicationFont(Raleway.SemiBold.str)

    gui = Leafify()
    gui.show()
    sys.exit(app.exec_())
