from dataclasses import dataclass
from functools import wraps
import random

from cached_property import cached_property

from qmltools import QmlWidget
from resourcely import ensure_field

from qml import FactWidget

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

    def fetch(self) -> list:
        new_records = []
        # fetch the remote data
        try:
            new_records = self.fetcher()
        except Exception as e:
            print(e)
            raise

        # if retrieval completed successfully
        # otherwise, keep previous records
        self.records = new_records
        return self.records

    def _build_widget(self, factobj, parent) -> QmlWidget:
        # build widget then return it
        return QmlWidget(
            dataobjs={ 'fact': factobj },
            qmlpath=FactWidget.url,
            parent=parent
        )

    @hotfetch
    def _build_fact(self):
        record = random.choice(self.records)
        return Fact(
            title=ensure_field(record, 'title'),
            content=ensure_field(record, 'content'),
            source=ensure_field(record, 'source'),
            data=record
        )

    @hotfetch
    def get(self) -> Fact:
        # Pull a random fact

        f = self._build_fact()

        self.served_facts += 1
        if self.served_facts > len(self.records):
            self.fetch()

        return f

    @hotfetch
    def get_widget(self) -> QmlWidget:
        # Return a fact directly bundled in a widget
        return self._build_widget(self.get())
    

@dataclass
class Fact:

    title: str
    content: str
    source: str
    data: dict
    factory: FactFactory

    def as_widget(self, parent) -> QmlWidget:
        return self.factory._build_widget(self, parent=parent)