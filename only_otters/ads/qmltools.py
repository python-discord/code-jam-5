import os

from PyQt5.QtWidgets import QWidget
from PyQt5.QtQuick import QQuickView
from PyQt5.QtCore import QUrl


def QmlWidget(dataobjs: dict, qmlpath: str, parent: QWidget):

    qmlpath = os.fspath(qmlpath)

    #
    view = QQuickView()
    engine = view.engine()

    for name, obj in dataobjs.items():
        engine.rootContext().setContextProperty(name, obj)

    #
    container = QWidget.createWindowContainer(view, parent)
    container.setStyleSheet("Widget { padding: 7px; }")
    view.setSource(QUrl(qmlpath))
    # Load widget

    return container
