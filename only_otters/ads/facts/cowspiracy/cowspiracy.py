from only_otters.ads.facts.fact import Fact, FactFactory
from only_otters.scrapetools.hquery import HierarchicalXPathQuery
from only_otters.ads.qml import FactWidget as qmlFactWidget
from only_otters.ads.qmltools import QmlWidget
from only_otters.resourcely import ensure_field

import spacy

NLP = spacy.load('en')

import re

from pathlib import Path

__folder__ = Path(__file__).parent


class CowspicaryFactFactory(FactFactory):

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
            _title='Did you know that ...',
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
    doc = NLP(item)
    v = {'VBP', 'VBZ', 'MD'} & {token.tag_ for token in doc}
    # if not v:
    #     print('rejected:', item, [(token.text, token.tag_, token.pos_) for token in doc])
    return v
