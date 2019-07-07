# Gentle Gnomes

![](./src/static/images/logo.svg)

## Description

You can search for any city in the United States and get climate change data for
that city. The data consists of indicators, which are different climate related
phenomenon such as temperature and precipitation. Each indicator uses both
historical and predictive data, the latter coming from the
[RCP8.5 scenario](https://skepticalscience.com/rcp.php), making the total range
1950-2100. The data shown as a scatter plot and the percent change is given.

### Implementation

The data is retrieved from the
[Azavea Climate API](https://docs.climate.azavea.com/index.html). The web
framework used is [Quart](https://pgjones.gitlab.io/quart/index.html). The front
end was done using [Bootstrap](https://getbootstrap.com/).

The Azavea Climate API has kind of brutal rate limits. Sorry if you end up
waiting a minute for a search!

## Installation

### Requirements

* Python 3.7
* [Poetry](https://poetry.eustace.io/docs/#installation)
* [Google Places API Key](https://developers.google.com/maps/documentation/javascript/get-api-key)
* [Azavea Climate API Token](https://docs.climate.azavea.com/index.html#getting-a-token)

### Setup
```bash

poetry install  # --no-dev if production
```

Create the file `gentle_gnomes/instance/config.py` with the following contents:

```py
AZAVEA_TOKEN = 'your_token'
GOOGLE_KEY = 'your_key'
```

### Run

```bash
poetry run start
```

### Test

```bash
poetry run pytest
```

## Attributions

Logo by [Luis Prado](http://thenounproject.com/Luis/)
