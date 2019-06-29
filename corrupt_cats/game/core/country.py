import random

from .temperature import Temperature as t
from .utils.functions import rand, check_temp
from .constants import (
	MAX_TEMP, MIN_TEMP, MAX_POPULATION, MIN_POPULATION
)

class Country:
    def __init__(self):
    	self.start_temp = t(rand(MIN_TEMP, MAX_TEMP))
    	self.type = check_temp(self.start_temp, MAX_TEMP, MIN_TEMP)
    	self.population = rand(MIN_POPULATION, MAX_POPULATION)

for i in range(10):
    c = Country()
    print(c.__dict__)
