from typing import Dict


class PlanetaryEffects:
    def __init__(
        self, bio_diversity: int, temperature: int, co2: int, habitable_land: int
    ) -> None:
        self.bio_diversity = bio_diversity
        self.temperature = temperature
        self.co2 = co2
        self.habitable_land = habitable_land
