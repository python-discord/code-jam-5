import os
import importlib
import random
import pathlib

__folder__ = pathlib.Path(__file__).parent


# list available factories

def list_available_factories():
    
    ls = os.walk(__folder__)
    dirs = next(ls)[1]
    return [
        importlib.import_module(dir).__factory__
        for dir in dirs
    ]


FACTORIES = list_available_factories()
print(FACTORIES)

def pick_fact():
    factory = random.choice(FACTORIES)
    return factory.get()
    

def new_facts():
    # Generator over a random selection of factories
    while 1:
        yield pick_fact()


print(pick_fact())