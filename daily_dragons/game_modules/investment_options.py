# TODO convert to load from json
from .investment import Investment
from .organization import Organization
from .planetary_effects import PlanetaryEffects
from .policy import Policy
import json
from typing import Dict


class InvestmentOptions:
    def __init__(self) -> None:
        self.options = self.create_investements()

    def __str__(self) -> str:
        menu = []
        for key, i in self.options.items():
            menu.append(f"{key}: {i.organization.name}")
        return "\n".join(menu)

    def _parse_json(self, file_location: str) -> Dict:
        """Helper function to load a json and dump it to a dictionary"""
        with open(file_location, mode="r") as json_file:
            raw_json = json.loads(json_file.read())
        return raw_json

    def create_investements(self) -> Dict:
        """From a json file with CEOs, organization names and policies creates
            a dictionary of options for the player"""
        raw_json = self._parse_json("../resources/data/organizations.json")
        investement_list = []
        for entry in raw_json:
            org = Organization(entry["name"], entry["ceo"], entry["description"])
            policy_list = []
            for polices in raw_json["polices"]:
                planet_effects = PlanetaryEffects(
                    polices["bio"],
                    polices["temperature"],
                    polices["co2"],
                    polices["habitable_land"],
                )
                policy = Policy(
                    polices["name"],
                    polices["description"],
                    planet_effects,
                    polices["roi"],
                )
                policy_list.append(policy)
            new_investment = Investment(org, polices)
            investement_list.append(new_investment)

        investement_options = {}
        for index, investment in enumerate(investement_list):
            investement_options[str(index)] = investment

        return investement_options
