# local
from only_otters.facts import Fact, FactFactory
from only_otters.scrapetools.hquery import HierarchicalXPathQuery
from only_otters.qml import Counter as qmlCounter
from only_otters.qmltools import QmlWidget
from only_otters.facts.counter import FactCounter, counter
from only_otters.resourcely import ensure_field

# std
from pathlib import Path


__folder__ = Path(__file__).parent


"""
An application of the Remote Resource template to URL:
https://www.theworldcounts.com/themes/our_environment
"""


class TheWorldCountsFactFactory(FactFactory):
    """FactFactory implementation for the website https://www.theworldcounts.com."""
    def __init__(self):
        super().__init__()
        self.fetcher = HierarchicalXPathQuery.from_yml(__folder__ / 'theworldcounts.yml')

    def _build_widget(self, factobj: Fact, parent) -> QmlWidget:
        return QmlWidget(
            qmlpath=qmlCounter.url,
            context={'fact_counter': factobj},
            parent=parent
        )

    def _build_fact(self, record: dict) -> FactCounter:

        start = float(ensure_field(record, 'start'))
        offset = float(ensure_field(record, 'cursor'))

        offset, inter = counter(start, offset, mininterval=20)
        inter = inter * 1000

        return FactCounter(
            value=start,
            offset=offset,
            interval=inter,
            precision=int(ensure_field(record, 'precision')),
            content=ensure_field(record, 'title') + ', ' + ensure_field(record, 'subtitle').lower(),
            source=self.fetcher.url,
            factory=self
        )


__factory__ = TheWorldCountsFactFactory()
__factory__.tags = ['counter', 'ui']


@__factory__.fetcher.pipe
def postprocess(item: dict) -> dict:
    """Postprocess a counter to extract data at a more granular level that hquery allows for."""
    for key in item:
        item[key] = item[key].strip()

    if item['figure'] == 'loading...':
        item['figure'] = None

    if item['cursor'].count(',') == 1:
        item['cursor'] = None
        item['start'] = None
        item['precision'] = None
    else:
        try:
            item['cursor'] = float(item['cursor'].split(',')[1])
            item['start'] = float(item['start'].split(',')[0].split('(')[1])
            item['precision'] = item['precision'].split(',')[2].strip()
        except (IndexError, ValueError):
            item['cursor'] = None
            item['start'] = None
            item['precision'] = None

    return item


@__factory__.fetcher.pipe
def valid(item: str) -> bool:
    """Ensure the item is a valid counter."""
    return item['start'] is not None
