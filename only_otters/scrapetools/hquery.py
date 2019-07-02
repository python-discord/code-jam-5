import re
from lxml import html as lhtml
import json
from functools import wraps, partial

from util import one_or_many


spec_ops = {
    'TAIL': lambda r: r.tail
}


"""
A module to write hierarchical queries to perform scraping.
"""


def resolve_xpath(element, expr):

    # specials = re.findall(r'{[A-Z]+}', expr)
    # expr = re.sub(r'{[A-Z]+}', '', expr)

    result = element.xpath(expr)

    # for sp in specials:
    #     sp = sp.strip('{').strip('}')
    #     op = spec_ops[sp]
    #     result = map(op, result)
    # result = list(result)

    return result


def pipe(*fns):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*a, **kw):
            r = fn(*a, **kw)
            for f in fns:
                r = f(r)
            return r
        return wrapper
    return decorator


def astype(typename):
    
    try:
        type_ = globals()[typename]
    except KeyError:
        raise

    if not callable(type_):
        raise UserWarning("{!r} is not a callable.".format(type_))

    return type_


PIPES = {
    'single': one_or_many,
    'astype': astype
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
        return pipe(*pipes)(fn)

    return fn


def deep_xpath(tree, xquery, **properties):

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
                value = [*deep_xpath(loc, value, **propagated_properties)]

            elif type(value) in (list, tuple):
                value = [
                    process_xpath(loc, v)
                    for v in value
                ]

            else:
                value = process_xpath(loc, value)

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
        'loc': '/html/body/ul/li',
        'properties': {
            'pipes': {
                # 'single': { 'default': None }
            },
            # 'propagate_properties': True
        },
        'query': {
            'text': 'text()',
            'contents': {
                'loc': 'ul/li',
                'query': {
                    'text': 'text()'
                }
            }
        }
    }

    a = deep_xpath(tree, xquery)
    print(tree.xpath('/html/body/ul/li/text()'))
    print(json.dumps([*a], indent=4))