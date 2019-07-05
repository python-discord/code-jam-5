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

from .qtobjcounter import FactCounter, Counter

from .qmltools import QmlWidget


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

        self.new_fact_button = QtWidgets.QPushButton('New')
        self.new_fact_button.clicked.connect(self.x)

        self.main_layout.addWidget(self.new_fact_button)

        self.main_widget.setLayout(self.main_layout)

    def new_widget(self, w):
        self.main_layout.addWidget(w)

    def x(self):
    
        from .facts import pick_fact

        fact = pick_fact()
        widget = fact.as_widget(parent=self)
        self.new_widget(widget)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    
    font_path = Path('../fonts')
    QtGui.QFontDatabase.addApplicationFont(str(font_path / 'Raleway-Regular.ttf'))
    
    win = TestWin()


    qml_file = 'qml/Counter.qml'
    # qmlRegisterType(FactCounter, 'FactCounter', 1, 0, FactCounter.__name__)

    # fc = FactCounter(99590, 15, 200, 0)
    # container =  QmlWidget(
    #     { 'fact_counter': fc },
    #     qmlpath=qml_file,
    #     parent=win
    # )

    win.show()

    e = app.exec_()

    sys.exit(e)