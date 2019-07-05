emissions = {
    # 6.0km/L, 16km both ways
    # How many times do you drive in a week?
    "driving": 12.3,
    # 240L wheelie bins, 0.2kg/L average density of landfill before processing, 1.9kg CO2 produced
    # How many wheelie bins do you fill up in a week?
    "rubbish": 91.2,
    # 0.11kg of CO2 per cup
    # How many coffees do you drink a day?
    "coffee": 0.77,
    # 0.2kg of CO2 per minute of showering
    # How long is your average shower?
    "shower": 1.4,
    # 0.05kg per hour of usage
    # How many hours do you use your laptop every day?
    "laptop": 0.35,
    # 2.4kg per hour, 2 hours per cycle
    # How many times do you use your dishwasher in a week?
    "dishwasher": 4.8
}


def total_footprint(actions=None):
    if actions is None:
        actions = {}

    footprint = 0

    for (k, v) in actions.items():
        footprint += emissions[k] * v

    return footprint
