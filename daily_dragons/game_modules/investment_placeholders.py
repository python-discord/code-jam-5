from .investment import Investment
from .organization import Organization
from .planetary_effects import PlanetaryEffects


# TODO: convert to json rather than hard coded placeholders
def investments():
    # Placeholder organizations :D
    # I think we could store this info in a json file that then
    # can be parsed to initialize all the possible investments
    invest_dict = {}

    bad_effects = PlanetaryEffects(-100, 0.02, 20, -100)
    evil_corp = Organization(
        "Faux News",
        (
            "Evil news corp that spreads lies and misinformation\n"
            "to benifit companies for the sake of profit of the\n"
            "global elite"
        ),
    )
    invest_dict["1"] = Investment(evil_corp, bad_effects)

    temp_effects = PlanetaryEffects(0, -0.02, -20, 0)
    nuke_ngo = Organization(
        "Nuke the Whales",
        (
            "Lobby group and think tank promoting using Nuclear\n"
            "energy as gap filler technology until renewables\n"
            "can fully supply the worlds energy needs"
        ),
    )
    invest_dict["2"] = Investment(nuke_ngo, temp_effects)

    acre_effects = PlanetaryEffects(100, 0, 0, 100)
    rain_ngo = Organization(
        "The Fellowship of the Rainforst",
        (
            "Lobby group trying to save the rainforest.\n"
            "They are often critized for their 'guerilla' tactics\n"
            "but have been successful in mitigating impacts from\n"
            "deforestation."
        ),
    )
    invest_dict["3"] = Investment(rain_ngo, acre_effects)

    return invest_dict
