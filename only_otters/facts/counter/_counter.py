from only_otters.facts import FactFactory
from only_otters.qmltools import QmlWidget

from typing import Union

from PyQt5.QtCore import QObject, pyqtProperty


class FactCounter(QObject):

    def __init__(
        self,
        value: Union[int, float],
        offset: Union[int, float],
        interval: int,
        precision: int,
        content: str,
        source: str,
        factory: FactFactory
    ):

        QObject.__init__(self)

        self._value = value
        self._offset = offset
        self._interval = interval
        self._precision = precision
        self._content = content
        self._source = source
        self.factory = factory

    @pyqtProperty(float, constant=True)
    def value(self) -> float:
        return self._value

    @pyqtProperty(float, constant=True)
    def offset(self) -> float:
        return self._offset

    @pyqtProperty(int, constant=True)
    def interval(self) -> int:
        return self._interval

    @pyqtProperty(int, constant=True)
    def precision(self) -> int:
        return self._precision

    @pyqtProperty('QString', constant=True)
    def content(self) -> str:
        return self._content

    @pyqtProperty('QString', constant=True)
    def source(self) -> str:
        return self._source

    def as_widget(self, parent) -> QmlWidget:
        return self.factory._build_widget(self, parent=parent)
