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
import os

from qtobjcounter import FactCounter, Counter


@contextmanager
def enter(type_, owner):
    obj = type_(owner)
    yield obj
    owner.addWidget(obj)


def QmlWidget(dataobjs: dict, qmlpath: str, parent: QtWidgets.QWidget):

    qmlpath = os.fspath(qmlpath)

    #
    view = QQuickView()
    engine = view.engine()

    for name, obj in dataobjs.items():
        engine.rootContext().setContextProperty(name, obj)

    #
    container = QtWidgets.QWidget.createWindowContainer(view, parent)
    container.setMinimumSize(300, 300)
    container.setMaximumSize(300, 300)
    view.setSource(QUrl(qml_file))
    # Load widget

    return container


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


    qml_file = 'Counter.qml'
    # qmlRegisterType(FactCounter, 'FactCounter', 1, 0, FactCounter.__name__)

    fc = FactCounter(1000, 1, 200, 0)
    # fc = Counter(1000, 1, 200, 0)
    # fc = FactCounter(value=1000, offset=1, interval=200, precision=0)
    # fc = Counter(value=1000, offset=1, interval=200, precision=0)

    container =  QmlWidget(
        { 'fact_counter': fc },
        qmlpath=qml_file,
        parent=win
    )

    win.show()

    e = app.exec_()

    print(fc.value)

    sys.exit(e)