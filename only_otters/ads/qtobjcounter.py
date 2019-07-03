import sys
from dataclasses import dataclass
import inspect
from functools import partial, wraps
import copy

# https://stackoverflow.com/questions/49479603/generating-pyqtproperty-methods

# https://stackoverflow.com/questions/52290153/qml-unable-to-assign-undefined-to
# https://www.riverbankcomputing.com/static/Docs/PyQt5/qt_properties.html

from PyQt5.QtCore import pyqtProperty, pyqtSignal, QObject

from dataqobject import dataqobject


@dataqobject
class Counter:

    value: float
    offset: float
    interval: int = 1000
    precision: int = 0


class FactCounter(QObject):

    # value: float
    # offset: float
    # interval: int = 1000
    # precision: int = 0

    def __init__(self, value, offset, interval=1000, precision=0):
        QObject.__init__(self)
        
        self._value = value
        self._offset = offset
        self._interval = interval
        self._precision = precision

    @pyqtProperty(float, constant=True)
    def value(self):
        return self._value

    @pyqtProperty(float, constant=True)
    def offset(self):
        return self._offset

    @pyqtProperty(int, constant=True)
    def interval(self):
        return self._interval

    @pyqtProperty(int, constant=True)
    def precision(self):
        return self._precision

    @property
    def x(self):
        return "bb"


FactCounter.x = pyqtProperty('QString',
    constant=True,
    fget=lambda s: "aa"
)

# FactCounter.x = 


if __name__ == "__main__":

    # Counter.x = lambda self: self.value
    
    c = Counter(
        _value=3,
        _offset=2
    )

    print(Counter)
    print(dir(c))
    print(c)
    print(c.value)