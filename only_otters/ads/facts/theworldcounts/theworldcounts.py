import json
from pathlib import Path

__folder__ = Path(__file__).parent

# import sys
# sys.path.append('../../..')

from only_otters.scrapetools.hquery import HierarchicalXPathQuery
from only_otters.scrapetools import autobrowser

from only_otters.ads.facts.fact import Fact, FactFactory

"""
An application of the Remote Resource template to URL:
https://www.theworldcounts.com/themes/our_environment
"""


FFF = None


@HierarchicalXPathQuery.pipe
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
            item['cursor'] = item['cursor'].split(',')[1]
            item['start'] = item['start'].split(',')[0].split('(')[1]
            item['precision'] = item['precision'].split(',')[2].strip()
        except IndexError:
            item['cursor'] = None
            item['start'] = None
            item['precision'] = None

    return item


if __name__ == "__main__":

    hxq = HierarchicalXPathQuery.from_yml(__folder__ / 'theworldcounts.yml')

    pulled_resources = [ *hxq() ]

    print(json.dumps(
        pulled_resources,
        indent=4
    ))

    if autobrowser.DRIVER is not None:
        autobrowser.DRIVER.close()