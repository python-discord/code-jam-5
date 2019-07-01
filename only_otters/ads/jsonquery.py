# from x import *

# path = header.has(cls)["interface-top"] / span / tail
import re
from lxml import html as lhtml
import json
from ad_resource import one_or_many


spec_ops = {
    'TAIL': lambda r: r.tail
}


def resolve_xpath(element, expr):

    specials = re.findall(r'{[A-Z]+}', expr)
    expr = re.sub(r'{[A-Z]+}', '', expr)

    result = element.xpath(expr)

    for sp in specials:
        sp = sp.strip('{').strip('}')
        op = spec_ops[sp]
        result = map(op, result)

    result = list(result)

    return one_or_many(result)


def deep_xpath(tree, xquery):

    container_query, query = xquery['container'], xquery['query']

    print(query)

    container = tree.xpath(container_query)

    for container in container:

        result = {}

        for key, value in query.items():

            if type(value) == dict:
                value = [*deep_xpath(container, value)]

            elif type(value) in (list, tuple):
                value = [
                    resolve_xpath(container, v)
                    for v in value
                ]

            else:
                value = resolve_xpath(container, value)

            result[key] = value


        yield result



if __name__ == "__main__":
    
    html = """
    <html>
        <body>
            <ul>
                <li> t <ul> <li> a </li> <li> <span> du </span> b </li> </ul> x </li>
                <li> r <ul> <li> c </li> <li> <span> ds </span> d </li> </ul> y </li>
            </ul>
        </body>
    </hthml>
    """

    tree = lhtml.fromstring(html)

    xquery = {
        'container': '/html/body/ul/li',
        'query': {
            'text': 'text()',
            'contents': {
                'container': 'ul/li',
                'query': {
                    'text': 'text()'
                }
            }
        }
    }

    a = deep_xpath(tree, xquery)
    print(tree.xpath('/html/body/ul/li/text()'))
    print(json.dumps([*a], indent=4))