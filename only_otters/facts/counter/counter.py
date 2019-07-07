from PyQt5.QtCore import QObject, pyqtProperty


class FactCounter(QObject):

    def __init__(self, value, offset, interval=1000, precision=0, text='', source=None, factory=None):
        
        QObject.__init__(self)
        
        self._value = value
        self._offset = offset
        self._interval = interval
        self._precision = precision
        self._text = text
        self._source = source
        self.factory = factory


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

    @pyqtProperty('QString', constant=True)
    def text(self):
        return self._text

    @pyqtProperty('QString', constant=True)
    def source(self):
        return self._source

    def as_widget(self, parent):
        return self.factory._build_widget(self, parent=parent)
