import requests
from lxml import html
from dataclasses import dataclass
import json
import re
from functools import partial, wraps

from cachetools.func import ttl_cache, lru_cache


def one_or_many(items: list, default=''):
    if items:
        if len(items) == 1:
            return items[0]
        return items
    return default

@lru_cache()
def cached_xpath(tree, query):
    return one_or_many(tree.xpath(query))


@ttl_cache(ttl=15)
def cached_request(source):
    # TODO: Enable scraping through selenium for dynamic pages
    response = requests.get(source)
    with open('ff.f', 'w+') as f:
        f.write(response.content.decode('utf-8'))
    return html.fromstring(response.content), response


def dictquery(element, query):
    return {
        key: cached_xpath(element, expr)
        for key, expr in query.items()
    }


@dataclass
class Resource:
    """
    An interface to describe a remote resource that can be hot-retrieved.
    """

    source: str
    query: dict
    container: str = None
    postprocess: callable = None

    def fetch(self):

        root, _ = cached_request(self.source)

        if root is None:
            raise UserWarning  # TODO: Add a proper exception

        if self.container is not None:
            roots = cached_xpath(root, self.container)

            if not roots:
                raise UserWarning  # TODO: Add a proper exception

            for element in roots:
                yield dictquery(element, self.query)

        else:
            return dictquery(root, self.query)


    def __call__(self):

        fetched = self.fetch()

        if self.postprocess is None:
            return fetched

        return map(self.postprocess, fetched)


def safestrmanip(*excpts):
    excpts = excpts or (IndexError,)
    def decorator(fn):
        @wraps(fn)
        def wrapper(text):
            try:
                return fn(text)
            except excpts as e:
                print(e)
                return text
        return wrapper
    return decorator


def postprocess(item):

    for key in item:
        item[key] = item[key].strip()

    try:
        item['cursor'] = item['cursor'].split(',')[1]
        item['start'] = item['start'].split(',')[0].split('(')[1]
    except IndexError:
        pass
        item['cursor'] = None
        item['start'] = None

    return item


if __name__ == "__main__":

    r = Resource(
        source='https://www.theworldcounts.com/themes/our_environment',
        container='//div[@id="main"]//a[@class="counter-link"]/div[@class="row"]',
        query={
            # 'figure': 'div[1]/div[@class="counter-number"]/p/text()',
            'title': 'div[2]/div[@class="counter-title"]/h3/text()',
            'subtitle': 'div[2]/div[@class="counter-title"]/span/text()',
            'start': 'div[1]/div[@class="counter-number"]/script/text()',
            'cursor': 'div[1]/div[@class="counter-number"]/script/text()'
        },
        postprocess=postprocess
    )

    pulled_resources = [*r()]

    print(r)
    json.dump(
        pulled_resources,
        open('resourcetest.json', 'w+'),
        indent=4
    )

    print('Saved results')
