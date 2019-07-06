import os
import importlib
import random
import pathlib

__folder__ = pathlib.Path(__file__).parent


# list available factories

def list_available_factories():
    
    ls = os.walk(__folder__)
    dirs = next(ls)[1]
    print(__name__)
    return [
        importlib.import_module('.' + dir ,package=__name__).__factory__
        for dir in dirs
    ]


FACTORIES = list_available_factories()
print(FACTORIES)

def pick_fact():
    factory = random.choice(FACTORIES)
    return factory.get()


def get_fact():
    return pick_fact()


def get_fact_by_tags(*tags):
    tags = set(tags)
    eligible_factories = list(filter(
            lambda factory: tags & set(factory.tags),
            FACTORIES
        ))
    if not eligible_factories:
        raise UserWarning('No available factories for the provided tags %s' % tags)
    return random.choice(eligible_factories).get()


def get_text_fact():
    return get_fact_by_tags('text')


def new_facts():
    # Generator over a random selection of factories
    while 1:
        yield pick_fact()


print(pick_fact())