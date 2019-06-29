"""File where constants, such as MAX_TEMP and others are stored"""

import json
from .utils.functions import load_json

conf = load_json("config.json")

population = conf.get("population", {})
temp = conf.get("temp", {})

MAX_TEMP = temp.get('max', 30)
MIN_TEMP = temp.get('min', -30)
MAX_POPULATION = population.get('max', 10_000_000)
MIN_POPULATION = population.get('min', 10000)
