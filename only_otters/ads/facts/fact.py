# local
from only_otters.ads.qmltools import QmlWidget
from only_otters.ads.qml import FactWidget
from only_otters.scrapetools.hquery import HierarchicalXPathQuery

# std
from dataclasses import dataclass
from functools import wraps
import random
from typing import Any, Dict, List

# qt
from PyQt5.QtCore import pyqtProperty, QObject
from PyQt5.QtWidgets import QWidget


"""
TODO:
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
    """
    A decorator for FactFactory objects.
    Ensure that records have been fetched before proceeding.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.records:
            self.fetch()
        return method(self, *args, **kwargs)
    return wrapper


class FactFactory:
    """
    A wrapper tying 3 concepts together:
    * data scraping from a source with hquery;
    * translating the resulting records (dictionaries) into Fact objets with
    a few basic fields (title, content, source);
    * widget generation for a given fact.

    A random fact among the records can be accessed through the `get` method.

    Most methods are implemented already, and what remains needs to be left in the control
    of each source's implementation as these are the parts that may differ depending on the source.
    * interpreting the record retrieved by the fetcher, building a Fact object out of it;
    * widget generation from said Fact object; the widget used might depend on the nature of the
    data found at the source.

    """

    def __init__(self):
        self.records: List[Dict[str, Any]] = []
        self.tags: List[str] = []
        self.served_facts: int = 0
        self.fetcher: HierarchicalXPathQuery = None

    def fetch(self) -> list:

        self.served_facts = 0
        new_records: List[Dict[str, Any]] = []

        # fetch the remote data
        try:
            new_records = self.fetcher()
        except Exception as e:
            print(e)
            # TODO:
            raise

        self.records = list(new_records)
        return self.records

    def _build_widget(self, factobj: 'Fact', parent: QWidget) -> QmlWidget:
        """TODO:# build widget then return it"""
        return QmlWidget(
            dataobjs={'fact': factobj},
            qmlpath=FactWidget.url,
            parent=parent
        )

    def _build_fact(self, record: dict) -> 'Fact':
        """TODO"""
        raise NotImplementedError

    @hotfetch
    def get(self) -> 'Fact':
        """
        Return a random fact among the available records.
        Records are refreshed if a good amount of facts have
        already been served by the current factory.
        """
        self.served_facts += 1
        if self.served_facts >= len(self.records):
            self.fetch()

        record: dict = random.choice(self.records)
        fact: Fact = self._build_fact(record)

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

    def as_widget(self, parent: QWidget) -> QmlWidget:
        return self.factory._build_widget(self, parent=parent)

    @pyqtProperty('QString', constant=True)
    def title(self) -> str:
        return self._title

    @pyqtProperty('QString', constant=True)
    def content(self) -> str:
        return self._content

    @pyqtProperty('QString', constant=True)
    def source(self) -> str:
        return self._source
