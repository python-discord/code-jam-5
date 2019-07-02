# scrapetools/HQuery

Basic scraping is achieved through XPath path expressions :

```python
list_elements = html.xpath('//ul/li')
```

In this package

## A basic hierarchical query


```yaml
url: https://www.google.com
dynamic: True
content:

  loc: /html/body/ul/li

  properties:
    pipes:
      single:
        default: null
    propagate_properties: true

  query:
    text: text()
    id: $ { str, int, single } a/text()
    xid: $ l{ doubidou:external, lfilter:isnumeric, print, lmap:strip } a/text()
    contents:
      loc: ul/li
      query:
        text: text()
```

## Pipes

### Higher-order pipes
### Modes