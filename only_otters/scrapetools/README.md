# scrapetools/HQuery

Basic scraping is achieved through XPath path expressions :

```python
list_elements = html.xpath('//ul/li')
```

## Hierarchical queries

The basic idea of this package is to simplify the scraping of a page down to a
yaml file.

In said file, you can describe nested requests to form a hierarchical structure
for the scraping process to flesh out. A query object always has two fields:

* `loc` which is the element (or elements each) to retrieve information from. It is expected that there are several of these items, and that we want to extract specific fields from each of these:
* `query` the fields to extract and their relative XPath expressions:

```yaml
loc: //ul/li
query: 
  link: a/@href
  text: text()
```

If we parse a page with 2 `li` elements, the result will look like this:

```json
[
  { "link": "http://1.com", "text": "Awesome website here!" },
  { "link": "http://2.com", "text": "Awesome website n2 here!" }
]
```

A query field can itself point to a query object, allowing to nest queries and build
a hierarchical output structure from just your config file:

```yaml
loc: //u/li
query:
  text: text()

  links:
    loc: a
    query:
      value: @href
```
Result:
```json
[
  {
    "text": "Awesome website here!",
    "links": [
      { "link": "http://1.com" }
    ]
  },
  {
    "text": "Awesome website n2 here!",
    "links": [
      { "link": "http://2.com" }
    ]
  }
]
```

## Top-level definition

We wrap the query with an additional level describing the source to scrape data from:

```yaml
url: 'https://www.google.com'
dynamic: true
content:
  # top level query
```
Such a file can be fed to `HierarchicalXPathQuery.from_yml`.

## Extending scope with simple computation calls

To except the concept and allow the user to keep clear of writing code as much as possible, it is possible to precede a XPath expression with a special syntax, like so:

```
$ { function, function } //ul/li
```

### Prefix

The `prefix` field in a query definition allows you to apply a function to all fields in a request :

```yaml
  prefix: $ { singleOut }
  query: 
    title: $ { filter:isnumeric } => $ { singleOut, filter:isnumeric }
```

### Postfix

`postfix` on the other hand allow you operate of the **built object records**, which are the
results of the query.

```
  postfix: $ { postprocess }
```

## Higher-order modes & pipes

```coffeescript
$ { map:strip, map:upper } //ul/li/text()
```

or with the `m(map)` higher-order mode, which applies `map` to every function in the expression:

```coffeescript
$ m:{ strip, upper }
```

You can have several expressions like this, but beware that they will be concatenated and their modes combined:

```coffeescript
$ m:{ strip, upper } $ l{ title }
# is equivalent to
$ m:l{ strip, upper, title }
```

## Registering new pipes

`HierarchicalXPathQuery` has 2 class methods which allow you to add new pipes and higher-order pipes. 

A pipe function must take only one argument and return one result, while a higher order pipe function must take two: a function and a list of items and yield back the new items.


```python
from hquery import HierarchicalXPathQuery as hxq

@hxq.pipe
@hxq.pipe('ck')
def cookie(item):
  return 'cookie: %s' % item

# can be then used as $ { cookie } or $ { ck }

@hxq.high_pipe
def print_if(fn, items):
  for item in items:
    if fn(item):
      print(item)
    yield item

# $ { print_if:cookie }