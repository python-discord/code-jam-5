import sys
sys.path.append('../..')
from scrapetools.hquery import HierarchicalXPathQuery


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
