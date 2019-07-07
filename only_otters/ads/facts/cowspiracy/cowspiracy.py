# local
from only_otters.ads.facts.fact import Fact, FactFactory
from only_otters.ads.qml import FactWidget as qmlFactWidget
from only_otters.ads.qmltools import QmlWidget
from only_otters.resourcely import ensure_field
from only_otters.scrapetools.hquery import HierarchicalXPathQuery

# standard
from pathlib import Path
import re

# other
import spacy


__folder__ = Path(__file__).parent
NLP = spacy.load('en')


class CowspicaryFactFactory(FactFactory):
    """FactFactory implementation for the website cowspiracy.com."""
    def __init__(self):
        super().__init__()
        self.fetcher = HierarchicalXPathQuery.from_yml(__folder__ / 'cowspiracy.yml')

    def _build_widget(self, factobj: Fact, parent) -> QmlWidget:
        return QmlWidget(
            dataobjs={'fact': factobj},
            qmlpath=qmlFactWidget.url,
            parent=parent
        )

    def _build_fact(self, record):
        return Fact(
            _title='Did you know that ... ',
            _content=ensure_field(record, 'content'),
            _source=self.fetcher.url,
            data=record,
            factory=self
        )


__factory__ = CowspicaryFactFactory()
__factory__.tags = ['text', 'ui']


@__factory__.fetcher.pipe
def clean(item):
    """Remove trailing footnote references in fact content."""
    item = re.sub(r'\xa0\s*\[.*\]\s*$', '', item)
    item = item.replace('\xa0', '')
    return item


@__factory__.fetcher.pipe
def sound(item):
    """Only keep elements which contains coherent sentences."""
    return {'VBP', 'VBZ', 'MD'} & {token.tag_ for token in NLP(item)}


@__factory__.fetcher.pipe
def not_empty(record):
    return record['content'].strip()
