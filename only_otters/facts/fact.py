# local
from only_otters.qmltools import QmlWidget
from only_otters.qml import FactWidget
from only_otters.scrapetools.hquery import HierarchicalXPathQuery

# std
from dataclasses import dataclass
from functools import wraps
import random
from typing import Any, Dict, List

# qt
from PyQt5.QtCore import pyqtProperty, QObject
from PyQt5.QtWidgets import QWidget


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
        """Fetch the remote data through the Hquery object."""
        self.served_facts = 0
        new_records: List[Dict[str, Any]] = []

        # fetch the remote data
        try:
            new_records = self.fetcher()
        except Exception as e:
            new_records = [
                ErrorFact(
                    title='Error',
                    content='Could not retrieve remote data for source %s: (%s)%s' % (
                        self.fetcher.url, type(e), e),
                    source=self.fetcher.url,
                    exception=e,
                    factory=self
                )
            ]

        self.records = list(new_records)
        return self.records

    def _build_widget(self, factobj: 'Fact', parent: QWidget) -> QmlWidget:
        """Build a widget depending on the source and fact object."""
        return QmlWidget(
            qmlpath=FactWidget.url,
            context={'fact': factobj},
            parent=parent
        )

    def _build_fact(self, record: dict) -> 'Fact':
        """Build a Fact object from a dict record."""
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

        if isinstance(record, ErrorFact):
            return record

        fact: Fact = self._build_fact(record)

        return fact

    @hotfetch
    def get_widget(self) -> QmlWidget:
        """Return a fact directly bundled in a widget."""
        return self._build_widget(self.get())


@dataclass
class Fact(QObject):

    """
    A simple dataclass with its attributes exposed to QML.
    """

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


class ErrorFact(Fact):

    exception: Exception
    title: str
    content: str
    source: str
    factory: FactFactory

    def __init__(
        self,
        *,
        exception: Exception,
        title: str,
        content: str,
        source: str,
        factory: FactFactory
    ):

        super().__init__(
            _title=title,
            _content=content,
            _source=source,
            data={},
            factory=factory
        )

        self.exception = exception

    def as_widget(self, parent: QWidget) -> QmlWidget:
        return QmlWidget(
            qmlpath=FactWidget.url,
            context={'fact': self},
            parent=parent
        )
