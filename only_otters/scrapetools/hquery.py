import yaml
import requests
from lxml import html as lhtml
from functools import partial
import re

import scrapetools.util as util
import scrapetools.autobrowser as autobrowser

# import util
# import autobrowser


class HierarchicalXPathQuery:

    @classmethod
    def resolve_mode(cls, name, high=False):
        n = (cls.MODES if not high else cls.HIGHER_ORDER_MODES).get(name)
        if n is None:
            raise UserWarning('No such %smode: %s' % ('higher-order ' * high, name))
        return n

    @classmethod
    def resolve_pipe(cls, name):

        if ':' in name:
            ho_pipe, pipename = name.split(':', maxsplit=1)

            hon = cls.HIGHER_ORDER_PIPES.get(ho_pipe)
            n = cls.PIPES.get(pipename)

            if hon is None:
                raise UserWarning('No such high-order pipe: %s' % ho_pipe)

            if n is None:
                raise UserWarning('No such pipe: %s' % pipename)

            return partial(hon, n)

        n = cls.PIPES.get(name)
        if n is None:
            raise UserWarning('No such pipe: %s' % name)
        return n

    @classmethod
    def resolve_pipe_expr(cls, expr, pipe_prefix=None):

        if pipe_prefix is not None:
            expr = pipe_prefix + ' ' + expr
        print(expr)

        regex = r'^\s*\$\s*([a-z]:)?([a-z]+)?\s*{\s*((?:[\w:]+\s*[,]?\s*)+)\s*}'
        # => $ <modes>{ func, func, func, ... } <query>
        # see 'query.yml' for an example

        pipes = []
        modes = []
        ho_mode = None
        m = re.match(regex, expr)

        while m is not None:
            _ho_mode, _modes, _pipes = m.groups()

            # Resolve modes & pipes before runnning Xpath expr

            # Parse modes
            if _ho_mode is not None:
                _ho_mode = _ho_mode.strip(':')
                if len(_ho_mode) > 1 or ho_mode:
                    raise UserWarning('There can only be one \
                        mode of higher-order. %s' % ho_mode)
                ho_mode = cls.resolve_mode(_ho_mode, high=True)

            # Parse pipes
            _pipes = _pipes.split(',')
            _pipes = list(map(str.strip, _pipes))

            pipes.extend(_pipes or [])
            modes.extend(_modes or [])

            expr = expr[m.span()[1]:]
            m = re.match(regex, expr)

        # Resolve pipes + ho_mode
        for idx, pipename in enumerate(pipes):
            fn = cls.resolve_pipe(pipename)
            if ho_mode is not None:
                fn = partial(ho_mode, fn)
            pipes[idx] = fn

        for idx, mode in enumerate(modes):
            fn = cls.resolve_mode(mode)
            modes[idx] = fn

        return expr, pipes[::-1], modes, ho_mode



    @classmethod
    def resolve_xpath(cls, element, expr, pipe_prefix=None):

        expr, pipes, modes, _ = cls.resolve_pipe_expr(expr, pipe_prefix=pipe_prefix)

        result = element.xpath(expr)

        for pipe in pipes:
            result = pipe(result)

        for mode in modes:
            result = mode(result)

        return result

    PIPES = {
        'single': util.one_or_many,
        'astype': util.astype,
        'int': int,
        'float': float,
        'str': str,
        'list': list,
        'tuple': tuple,
        'flatten': util.flatten,
        'isnumeric': str.isnumeric,
        'isalpha': str.isalpha,
        'isalnm': str.isalnum,
        'print': lambda a: print(a) or a,
        'strip': str.strip,
        'upper': str.upper,
        'lower': str.lower,
        'title': str.title,
        'capitalize': str.capitalize,
        'is': lambda x: x,
        'bool': bool
    }

    HIGHER_ORDER_PIPES = {
        'map': map,
        'filter': filter,
        'lmap': lambda f, n: list(map(f, n)),
        'lfilter': lambda f, n: list(filter(f, n)),
        'lcomp': lambda f, n: [f(_) for _ in n]
    }

    MODES = {
        's': str,
        'l': list,
        'u': util.one_or_many
    }

    HIGHER_ORDER_MODES = {
        'm': lambda f, gen: list(map(f, gen)),
        'f': lambda f, gen: list(filter(f, gen))
    }

    @classmethod
    def register_pipe(cls, fn, name=None, high=False):

        if name is not None:
            if not re.match(r'^\w+$', name):
                raise UserWarning('{!r} is not a compliant name. \
                    Allowed characters: [a-zA-Z0-9_]'.format(name))

        if not high:
            cls.PIPES[name or fn.__name__] = fn
        else:
            cls.HIGHER_ORDER_PIPES[name or fn.__name__] = fn

    @classmethod
    def pipe(cls, name=None):  # A pipe decorator

        if callable(name):
            return cls.register_pipe(name)

        return partial(cls.register_pipe, name=name)

    @classmethod
    def high_pipe(cls, name=None):

        if callable(name):
            return cls.register_pipe(name, high=True)

        return partial(cls.register_pipe, name=name, high=True)

    @classmethod
    def apply_pipes(cls, fn, pipe_properties):

        pipes = []

        for name, kargs in pipe_properties.items():

            target = cls.PIPES.get(name)
            if target is None:
                raise KeyError('No such pipe function: %s' % name)

            pipes.append(
                partial(target, **kargs)
            )

        if pipes:
            return util.pipe(*pipes)(fn)

        return fn

    @classmethod
    def process_query(cls, tree, xquery, **properties):

        loc_query = xquery['loc']
        query = xquery['query']
        prefix = xquery.get('prefix')

        # Process properties
        properties = properties or {}
        properties.update(xquery.get('properties', {}))

        # Prepare to propagate properties to nested queries
        propagated_properties = {}
        if properties.get('propagate_properties'):
            propagated_properties = properties

        process_xpath = cls.resolve_xpath

        # Set up the pipes
        pipe_properties = properties.get('pipes')
        if pipe_properties is not None:
            process_xpath = cls.apply_pipes(cls.resolve_xpath, pipe_properties)

        if prefix is not None:
            process_xpath = partial(process_xpath, pipe_prefix=prefix)

        for loc in tree.xpath(loc_query):

            result = {}

            for key, value in query.items():

                if type(value) == dict:
                    value = [*cls.process_query(loc, value, **propagated_properties)]

                elif type(value) in (list, tuple):
                    value = [
                        process_xpath(loc, v)
                        for v in value
                    ]

                else:
                    value = process_xpath(loc, value)

                result[key] = value

            yield result

    @classmethod
    def from_yml(cls, filepath):
        data = yaml.safe_load(open(filepath))
        return cls(**data)

    def __init__(self, *, content, url=None, dynamic=False):

        self.url = url
        self.content = content
        self.dynamic = dynamic

    def get(self, url=None, dynamic=None):

        url = url or self.url

        if dynamic is None:
            dynamic = self.dynamic

        if dynamic:
            return autobrowser.fetch(url)

        response = requests.get(url)
        if response.status_code >= 400:
            raise requests.exceptions.HTTPError(response)

        return response.content

    def __call__(self, url=None, html=None):

        url = url or self.url

        if html is None:
            html = self.get(url)

        tree = lhtml.fromstring(html)

        return self.__class__.process_query(tree, self.content)


@HierarchicalXPathQuery.pipe
def external(item):
    print('EXTERNAL:', item)
    return item


@HierarchicalXPathQuery.high_pipe
def doubidou(fn, items):
    return ('X:' + fn(i) for i in map(str, items))


if __name__ == "__main__":

    text = open('test.html').read()
    hxq = HierarchicalXPathQuery.from_yml('query.yml')

    result = hxq(html=text)

    print(*result)
    hxq.get()
