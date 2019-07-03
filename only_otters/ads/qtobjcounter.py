import sys
from dataclasses import dataclass
import inspect
from functools import partial
import copy

# https://stackoverflow.com/questions/49479603/generating-pyqtproperty-methods

# https://stackoverflow.com/questions/52290153/qml-unable-to-assign-undefined-to
# https://www.riverbankcomputing.com/static/Docs/PyQt5/qt_properties.html

from PyQt5.QtCore import pyqtProperty, QCoreApplication, QObject, QUrl
from PyQt5.QtQml import qmlRegisterType, QQmlComponent, QQmlEngine


def resolve_type(type_):
    return {
        str: 'QString'
    }.get(type_, type_)


def make_getter(arg, type_):

    print(arg, '=>', type_)

    type_ = resolve_type(type_)

    # return pyqtProperty(type_)
    # return (
    #     partial(getattr, name=arg)
    # )
    return lambda self: getattr(self, arg)


def dataqobject(cls):

    # cls = copy.copy(cls)
    
    d = inspect.getfullargspec(cls.__init__)

    for arg in d.args[1:]:
        annotation = d.annotations[arg]
        getter = make_getter('_' + arg, annotation)
        setattr(cls, arg, getter)
        print(getattr(cls, arg))

    return cls


class QDataObject(QObject):

    def __init__(self):
        super().__init__()



# @dataqobject
# @dataclass
# class Counter(QDataObject):

#     value: float
#     offset: float
#     interval: int = 1000
#     precision: int = 0

#     @pyqtProperty(float)
#     def _value(self):
#         return value

#     @pyqtProperty(float)
#     def _offset(self)


# @dataclass
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


# if __name__ == "__main__":

#     # Counter.x = lambda self: self.value
    
#     c = Counter(
#         value=3,
#         offset=2
#     )

#     print(c)

#     print(getattr(Counter, '_value'))
#     print(Counter._value)
#     print(c._value())