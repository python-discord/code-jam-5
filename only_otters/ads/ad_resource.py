import requests
from lxml import html
from dataclasses import dataclass

from cachetools.func import ttl_cache, lru_cache


def one_or_many(items: list, ifempty=''):
    """
    Taking a list as input,
    return the first item if there is only one item,
    else return the 'ifempty' value is the list is empty,
    else return the initial list.
    """
    if items:
        if len(items) == 1:
            return items[0]
        return items
    return ifempty


@lru_cache()
def cached_xpath(tree, query):
    """Wraps the processing of a XPath query with a LRU (least-recently-used)
    cache to speed up query processing.

    :tree
    The lxml tree to process the query on.

    :query
    The XPath query. TODO: Verify terminology
    """
    return one_or_many(tree.xpath(query))


@ttl_cache(ttl=30)
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
            raise UserWarning('Request failed')  # TODO: Add a proper exception

        if self.container is not None:

            roots = cached_xpath(root, self.container)
            if not roots:
                raise UserWarning('Container not found')  # TODO: Add a proper exception

            for element in roots:
                yield dictquery(element, self.query)

        else:
            return dictquery(root, self.query)

    def __call__(self):

        fetched = self.fetch()

        if self.postprocess is None:
            return fetched

        return map(self.postprocess, fetched)
