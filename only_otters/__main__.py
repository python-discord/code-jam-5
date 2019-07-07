# locale
from .app import Leafify
from .fonts import Raleway

# std
from pathlib import Path
import sys

# qt
from PyQt5 import QtWidgets, QtGui


if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)

    QtGui.QFontDatabase.addApplicationFont(Raleway.Regular.str)
    QtGui.QFontDatabase.addApplicationFont(Raleway.SemiBold.str)

    gui = Leafify()
    gui.show()
    sys.exit(app.exec_())
