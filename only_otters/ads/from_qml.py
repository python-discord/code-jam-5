# https://www.youtube.com/watch?time_continue=388&v=JxfiUx60Mbg
# https://doc.qt.io/archives/qt-4.8/qml-integration.html
# https://stackoverflow.com/questions/31531961/how-to-integrate-qml-file-into-qt-widgets-app
# https://www.riverbankcomputing.com/static/Docs/PyQt5/qml.html

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtQuick import QQuickView
from PyQt5.QtCore import QUrl
from PyQt5.QtQml import qmlRegisterType, QQmlComponent, QQmlEngine
from pathlib import Path
import sys
from contextlib import contextmanager

from qtobjcounter import FactCounter


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
    view = QQuickView()
    engine = view.engine()
    qml_file = 'custCounter.qml'
    # qmlRegisterType(FactCounter, 'FactCounter', 1, 0, FactCounter.__name__)

    fc = FactCounter(1000, 1, 200, 0)
    engine.rootContext().setContextProperty('fact_counter', fc)

    #
    container = QtWidgets.QWidget.createWindowContainer(view, win)
    container.setMinimumSize(300, 300)
    container.setMaximumSize(300, 300)
    view.setSource(QUrl(qml_file))
    # Load widget

    win.show()

    e = app.exec_()

    print(fc.value)

    sys.exit(e)