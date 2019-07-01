from ad_resource import Resource
import json

"""
An application of the Remote Resource template to URL:
https://www.theworldcounts.com/themes/our_environment
"""


def postprocess(item):

    for key in item:
        item[key] = item[key].strip()

    if item['figure'] == 'loading...':
        item['figure'] = None

    if item['cursor'].count(',') == 1:
        item['cursor'] = None
        item['start'] = None
    else:
        try:
            item['cursor'] = item['cursor'].split(',')[1]
            item['start'] = item['start'].split(',')[0].split('(')[1]
        except IndexError:
            item['cursor'] = None
            item['start'] = None

    return item


template = Resource(
    source='https://www.theworldcounts.com/themes/our_environment',
    container='//div[@id="main"]//a[@class="counter-link"]/div[@class="row"]',
    query={
        'figure': 'div[1]/div[@class="counter-number"]/p/text()',
        'title': 'div[2]/div[@class="counter-title"]/h3/text()',
        'subtitle': 'div[2]/div[@class="counter-title"]/span/text()',
        'start': 'div[1]/div[@class="counter-number"]/script/text()',
        'cursor': 'div[1]/div[@class="counter-number"]/script/text()'
    },
    postprocess=postprocess
)


if __name__ == "__main__":

    pulled_resources = [*template()]

    print(template)
    print(json.dumps(
        pulled_resources,
        indent=4
    ))
