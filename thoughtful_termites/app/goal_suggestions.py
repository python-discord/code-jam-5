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
        'Take public transport, walk or a ride a bike on some days '
        'instead of driving.'
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

    GoalSuggestion(
        'Cook At Home',
        'Cook at home instead of ordering takeaway.'
    ),

    GoalSuggestion(
        'Hand Wash Clothes',
        'Hand wash clothes instead of using a washing machine.'
    ),

    GoalSuggestion(
        'Hand Wash Dishes',
        'Hand wash dishes instead of using a dish washer.'
    ),

    GoalSuggestion(
        'Take Shorter Showers',
        'Try to reduce time spent in the shower.'
    ),
)
"""
Collection of predefined suggestions.
"""

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
