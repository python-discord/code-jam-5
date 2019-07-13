"""File where constants, such as MAX_TEMP and others are stored"""

from .utils.functions import load_json

setup = load_json("game/setup.json")
conf = load_json("game/config.json")

population = setup.get("population", {})
temp = setup.get("start_temp", {})


class Constants:
    def __init__(self):

        self.MAX_TEMP = temp.get('max', 30)
        self.MIN_TEMP = temp.get('min', -30)

        self.MAX_POPULATION = population.get('max', 100_000_000)
        self.MIN_POPULATION = population.get('min', 500000)

        self.COUNTRY_AMOUNT = conf.get('country_amount', 10)

        self.SCREEN_WIDTH = 1024
        self.SCREEN_HEIGHT = 600
        self.SCREEN_TITLE = "CorruptClimate v.0.1"

        self.WATER_COLOR = (35, 137, 218, 255)


constants = Constants()
