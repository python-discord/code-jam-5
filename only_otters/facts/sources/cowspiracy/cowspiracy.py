# local
from only_otters.facts import Fact, FactFactory
from only_otters.qml import FactWidget as qmlFactWidget
from only_otters.qmltools import QmlWidget
from only_otters.resourcely import ensure_field
from only_otters.scrapetools.hquery import HierarchicalXPathQuery

# standard
from pathlib import Path
import re

# qt
from PyQt5.QtWidgets import QWidget

# other
import spacy


__folder__ = Path(__file__).parent
NLP = spacy.load('en')


class CowspicaryFactFactory(FactFactory):
    """FactFactory implementation for the website https://www.cowspiracy.com."""
    def __init__(self):
        super().__init__()
        self.fetcher = HierarchicalXPathQuery.from_yml(__folder__ / 'cowspiracy.yml')

    def _build_widget(self, factobj: Fact, parent: QWidget) -> QmlWidget:
        return QmlWidget(
            qmlpath=qmlFactWidget.url,
            context={'fact': factobj},
            parent=parent
        )

    def _build_fact(self, record: dict) -> Fact:
        return Fact(
            _title=record.get('title') or 'Did you know that ... ',
            _content=ensure_field(record, 'content'),
            _source=self.fetcher.url,
            data=record,
            factory=self
        )


__factory__ = CowspicaryFactFactory()
__factory__.tags = ['text', 'ui']


@__factory__.fetcher.pipe
def clean(item: str) -> str:
    """Remove trailing footnote references in fact content."""
    item = re.sub(r'\xa0\s*\[.*\]\s*$', '', item)
    item = item.replace('\xa0', '')
    return item


@__factory__.fetcher.pipe
def sound(item: str) -> bool:
    """Only keep elements which contains coherent sentences."""
    return {'VBP', 'VBZ', 'MD'} & {token.tag_ for token in NLP(item)}


@__factory__.fetcher.pipe
def not_empty(record: str) -> bool:
    return record['content'].strip()
