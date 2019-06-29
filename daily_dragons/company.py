from typing import Dict


class Company:
    def __init__(self, name: str, description: str, planetary_effects: Dict[str, int]):
        self.name = name
        self.description = description
        self.planetary_effects = planetary_effects
