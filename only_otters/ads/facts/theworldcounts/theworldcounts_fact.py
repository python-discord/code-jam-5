from only_otters.ads.facts.fact import Fact, FactFactory, hotfetch
from only_otters.scrapetools.hquery import HierarchicalXPathQuery
from only_otters.ads.qml import Counter as qmlCounter
from only_otters.ads.qmltools import QmlWidget
from only_otters.ads.qtobjcounter import FactCounter
from only_otters.resourcely import ensure_field
from only_otters.ads.counter import counter

from pathlib import Path

__folder__ = Path(__file__).parent



class TheWorldCountsFactFactory(FactFactory):

    def __init__(self):
        super().__init__()
        self.fetcher = HierarchicalXPathQuery.from_yml(__folder__ / 'theworldcounts.yml')

    def _build_widget(self, factobj: Fact, parent) -> QmlWidget:
        return QmlWidget(
            dataobjs={ 'fact_counter': factobj },
            qmlpath=qmlCounter.url,
            parent=parent
        )

    def _build_fact(self, record):
        # {
        # 'figure': None, 
        # 'title': 'World population', 
        # 'subtitle': 'Right now', 
        # 'start': '7677500838.070457', 
        # 'cursor': ' 2.538563344286236'}

        # TODO: Parse scientific notation in counter.py:raw
        # TODO: Remove None objs

        start = float(ensure_field(record, 'start'))
        offset = float(ensure_field(record, 'cursor'))

        print(start, offset)

        offset, inter = counter(start, offset, mininterval=20)
        inter = inter * 1000
        
        print(offset, inter)

        return FactCounter(
            value=start,
            offset=offset,
            interval=inter,
            precision=int(ensure_field(record, 'precision')),
            text=ensure_field(record, 'title')  + ', ' + ensure_field(record, 'subtitle').lower(),
            factory=self
        )
        

__factory__ = TheWorldCountsFactFactory()


@__factory__.fetcher.pipe # pipe should bind the pipe to an instance, not the class
def postprocess(item):

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
        except IndexError:
            item['cursor'] = None
            item['start'] = None
            item['precision'] = None

    return item


@__factory__.fetcher.pipe
def valid(item):
    return item['start'] is not None