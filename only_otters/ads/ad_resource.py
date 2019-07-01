import requests
from lxml import html
from dataclasses import dataclass
import json

from cachetools.func import ttl_cache, lru_cache


@lru_cache()
def cached_xpath(tree, query):
    return tree.xpath(query)


@ttl_cache(ttl=15)
def cached_request(url):
    # TODO: Enable scraping through selenium for dynamic pages
    response = requests.get(url)
    return html.fromstring(response.content), response


@dataclass
class Resource:
    """
    An interface to describe a remote resource that can be hot-retrieved.
    """

    url: str
    pattern: dict
    location: str = None

    def __call__(self):

        root, _ = cached_request(self.url)

        if root is None:
            raise UserWarning  # TODO: Add a proper exception

        if self.location is not None:
            roots = cached_xpath(root, self.location)

            if not roots:
                raise UserWarning  # TODO: Add a proper exception

            for element in roots:
                yield {
                    key: cached_xpath(element, expr)
                    for key, expr in self.pattern.items()
                }

        else:
            return {
                key: cached_xpath(root, expr)
                for key, expr in self.pattern.items()
            }


if __name__ == "__main__":

    r = Resource(
        url='https://www.theworldcounts.com/themes/our_environment',
        location='//div[@id="main"]//a[@class="counter-link"]/div[@class="row"]',
        pattern={
            'figure': 'div[1]/div/p/text()',
            'name': 'div[2]/div[@class="counter-title"]/h3/text()',
            'happening': 'div[2]/div[@class="counter-title"]/span/text()'
        }
    )

    pulled_resources = *r(),

    print(r)
    json.dump(
        pulled_resources,
        open('resourcetest.json', 'w+'),
        indent=4
    )

    print('Saved results')
