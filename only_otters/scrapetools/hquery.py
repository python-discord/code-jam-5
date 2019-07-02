import yaml
import requests
from lxml import html as lhtml
from functools import partial

import util


def resolve_xpath(element, expr):
    return element.xpath(expr)


PIPES = {
    'single': util.one_or_many,
    'astype': util.astype
}


def apply_pipes(fn, pipe_properties):

    pipes = []

    for name, kargs in pipe_properties.items():

        target = PIPES.get(name)
        if target is None:
            raise KeyError('No such pipe function: %s' % name)

        pipes.append(
            partial(target, **kargs)
        )

    if pipes:
        return util.pipe(*pipes)(fn)

    return fn


def process_query(tree, xquery, **properties):

    loc_query = xquery['loc']
    query = xquery['query']

    # Process properties
    properties = properties or {}
    properties.update(xquery.get('properties', {}))

    # Prepare to propagate properties to nested queries
    propagated_properties = {}
    if properties.get('propagate_properties'):
        propagated_properties = properties

    process_xpath = resolve_xpath

    # Set up the pipes
    pipe_properties = properties.get('pipes')
    if pipe_properties is not None:
        process_xpath = apply_pipes(resolve_xpath, pipe_properties)

    for loc in tree.xpath(loc_query):

        result = {}

        for key, value in query.items():

            if type(value) == dict:
                value = [*process_query(loc, value, **propagated_properties)]

            elif type(value) in (list, tuple):
                value = [
                    process_xpath(loc, v)
                    for v in value
                ]

            else:
                value = process_xpath(loc, value)

            result[key] = value

        yield result


class HierarchicalXPathQuery:

    @classmethod
    def from_yml(cls, filepath):
        data = yaml.safe_load(open(filepath))
        return cls(**data)

    def __init__(self, *, content, url=None, dynamic=False):

        self.url = url
        self.content = content
        self.dynamic = dynamic

    def __call__(self, url=None, html=None):

        url = url or self.url

        if html is None:

            response = requests.get(self.url)

            if response.status_code >= 400:
                raise requests.exceptions.HTTPError(response)

            html = response.content

        tree = lhtml.fromstring(html)

        return process_query(tree, self.content)


if __name__ == "__main__":

    text = open('test.html').read()
    hxq = HierarchicalXPathQuery.from_yml('query.yml')

    result = hxq(html=text)
    print(*result)
