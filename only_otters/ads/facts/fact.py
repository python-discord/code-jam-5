from dataclasses import dataclass
from functools import wraps
import random

from only_otters.ads.qmltools import QmlWidget

from only_otters.ads.qml import FactWidget

from PyQt5.QtCore import pyqtProperty, QObject

"""
The idea is to have each source inherit from the following classes.

Each source module has its own unique FactFactory object '__factory__', which yields
Fact objects.

A fact object has 4 fields at the least:
* title
* content
* source (url)
* data (the original record)

+ the factory it originates from.

f = Fact()

f.widget (property)
should return a widget to display the fact in the interface.
There should be a default widget with {title, content, source}
if the source factory doesn't specify one


And all this wrapped in

from facts import new_facts


"""


def hotfetch(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.records:
            self.fetch()
        return method(self, *args, **kwargs)
    return wrapper


class FactFactory:

    def __init__(self):
        self.records = []
        self.served_facts = 0
        self.tags = []
        self.fetcher = None

    def fetch(self) -> list:
        
        new_records = []

        # fetch the remote data
        try:
            new_records = self.fetcher()
        except Exception as e:
            print(e)
            # TODO:
            raise

        self.records = list(new_records)
        return self.records

    def _build_widget(self, factobj, parent) -> QmlWidget:
        # build widget then return it
        return QmlWidget(
            dataobjs={'fact': factobj},
            qmlpath=FactWidget.url,
            parent=parent
        )

    def _build_fact(self, record: dict):
        raise NotImplementedError

    @hotfetch
    def get(self):

        self.served_facts += 1
        if self.served_facts >= len(self.records):
            self.fetch()

        record = random.choice(self.records)
        fact = self._build_fact(record)

        return fact

    @hotfetch
    def get_widget(self) -> QmlWidget:
        """Return a fact directly bundled in a widget."""
        return self._build_widget(self.get())


@dataclass
class Fact(QObject):

    _title: str
    _content: str
    _source: str
    data: dict
    factory: FactFactory

    def __post_init__(self):
        QObject.__init__(self)

    def as_widget(self, parent) -> QmlWidget:
        return self.factory._build_widget(self, parent=parent)

    @pyqtProperty('QString', constant=True)
    def title(self):
        return self._title

    @pyqtProperty('QString', constant=True)
    def content(self):
        return self._content

    @pyqtProperty('QString', constant=True)
    def source(self):
        return self._source
