# std
import os

# qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtQuick import QQuickView
from PyQt5.QtCore import QUrl


def QmlWidget(qmlpath: str, context: dict, parent: QWidget) -> QWidget:
    """
    Generate a QtWidgets widget from a QML file.
    
    :qmlpath
    The pat of the QML file.

    :context
    The context objects to expose to QML.
    """

    qmlpath = os.fspath(qmlpath)

    view = QQuickView()
    engine = view.engine()

    for name, obj in context.items():
        engine.rootContext().setContextProperty(name, obj)

    container = QWidget.createWindowContainer(view, parent)
    container.setStyleSheet("Widget { padding: 7px; }")
    view.setSource(QUrl.fromLocalFile(qmlpath))

    return container
