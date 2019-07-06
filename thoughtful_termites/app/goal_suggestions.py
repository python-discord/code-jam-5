# import random


class GoalSuggestion:
    """
    This class describes an individual suggestion for a goal.
    """

    name = None
    """Name of the goal."""

    desc = None
    """Description of the goal."""

    more_info = None
    """
    Additional goal info.
    i.e. a link showing why this goal helps reduce carbon footprint.
    """

    def __init__(
            self,
            name,
            desc,
            more_info=None,
    ):
        self.name = name
        self.desc = desc
        self.more_info = more_info


suggestions = (
    GoalSuggestion(
        'Drive Less',
        'Take public transport or a bike ride on some days instead of '
        'driving.'
    ),

    GoalSuggestion(
        'Unplug Devices',
        'Unplug unused devices when they don\'t need power.'
    ),

    GoalSuggestion(
        'Use Less Heating',
        'Wear more layers of clothing/warmer clothes instead of running '
        'heating appliances.'
    ),

    GoalSuggestion(
        'Line Dry Clothes',
        'Use a line to dry your clothes instead of a dryer.'
    ),
)
"""
Collection of predefined suggestions.
"""


# def random_suggestion_generator():
#     while True:
#         shuffled = random.sample(suggestions, len(suggestions))
#         yield from shuffled
#
#
# suggestion_generator = random_suggestion_generator()
#
#
# def random_suggestion() -> GoalSuggestion:
#     global suggestion_generator
#     while True:
#         try:
#             return next(suggestion_generator)
#         except StopIteration:
#             suggestion_generator = random_suggestion_generator()

_suggestions_iterator = iter(suggestions)


def get_suggestion():
    """
    A convenience function for getting a single suggestion.

    :return: A suggestion object.
    """
    global _suggestions_iterator

    while True:
        try:
            return next(_suggestions_iterator)
        except StopIteration:
            _suggestions_iterator = iter(suggestions)
