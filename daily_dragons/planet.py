from typing import Dict
from planetary_effects import PlanetaryEffects


class Planet:
    """Track the planets health with key statistics"""

    def __init__(
        self,
        bio_diversity: int = 0,
        temperature: int = 0,
        co2: int = 0,
        habitable_land: int = 0,
    ) -> None:
        """Track the stats as a net change from baseline

        bio diversity tracks the change in the total number of species
        tempature is the change in C (celsius)
        co2 is tracked in ppm (parts per million)
        habitable land is in hectacres (100 acres)

        """
        self.bio_diversity = bio_diversity
        self.temperature = temperature
        self.co2 = co2
        self.habitable_land = habitable_land

    @property
    def scoreboard(self) -> Dict[str, str]:
        """A dict of the stats for easy output by gui"""
        current_stats = {
            "bio_diversity": str(self.bio_diversity),
            "temperature": str(self.temperature),
            "co2": str(self.co2),
            "habitable_land": str(self.habitable_land),
        }

        return current_stats

    def affect_planet(self, effects: PlanetaryEffects) -> None:
        """Applies the changes of an effect in place to the planet"""
        self.bio_diversity += effects.bio_diversity
        self.temperature += effects.temperature
        self.co2 += effects.co2
        self.habitable_land += self.habitable_land

    def __str__(self) -> str:
        current_stats = (
            f"bio_diversity: {str(self.bio_diversity)} \n"
            f"temperature: {str(self.temperature)} \n"
            f"co2: {str(self.co2)} \n"
            f"habitable_land: {str(self.habitable_land)} \n"
        )

        return current_stats
