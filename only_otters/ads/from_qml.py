# https://www.youtube.com/watch?time_continue=388&v=JxfiUx60Mbg
# https://doc.qt.io/archives/qt-4.8/qml-integration.html
# https://stackoverflow.com/questions/31531961/how-to-integrate-qml-file-into-qt-widgets-app
# https://www.riverbankcomputing.com/static/Docs/PyQt5/qml.html

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtQuick import QQuickView
from PyQt5.QtCore import QUrl
from pathlib import Path
import sys
from contextlib import contextmanager

@contextmanager
def enter(type_, owner):
    obj = type_(owner)
    yield obj
    owner.addWidget(obj)


class TestWin(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setMinimumSize(640, 480)
        self.setup()

    def setup(self, main=None):
        self.main_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.main_widget.setLayout(self.main_layout)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    
    font_path = Path('../fonts')
    QtGui.QFontDatabase.addApplicationFont(str(font_path / 'Raleway-Regular.ttf'))
    
    win = TestWin()

    #
    qml_file = 'Counter.qml'
    view = QQuickView()
    container = QtWidgets.QWidget.createWindowContainer(view, win)
    container.setMinimumSize(300, 300)
    container.setMaximumSize(300, 300)
    view.setSource(QUrl(qml_file))
    # Load widget

    win.show()
    sys.exit(app.exec_())