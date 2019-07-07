import os
import importlib
import random
import pathlib


__folder__ = pathlib.Path(__file__).parent


def list_available_factories():
    """Retrieve the list of available factories in the package."""
    ls = os.walk(__folder__)
    dirs = next(ls)[1]
    return [
        importlib.import_module('.' + dir, package=__name__).__factory__
        for dir in dirs
    ]

print('Initializing fact factories...')
FACTORIES = list_available_factories()


def pick_fact():
    """Pick a random fact from a randomly chosen factory."""
    factory = random.choice(FACTORIES)
    return factory.get()


def get_fact_by_tags(*tags):
    """Filters the eligible factories by tag and pick a fact from the resulting list."""
    tags = set(tags)

    eligible_factories = [
        f for f in FACTORIES
        if tags & set(f.tags)
    ]

    if not eligible_factories:
        raise UserWarning('No available factories for the provided tags: %s' % tags)

    return random.choice(eligible_factories).get()


def get_text_fact():
    return get_fact_by_tags('text')
