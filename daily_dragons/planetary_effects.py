from typing import Dict


class PlanetaryEffects:
    """
    PlanetaryEffects

    Helper class for changing the affects player decisions have on the planet
    """

    def __init__(
        self, bio_diversity: int, temperature: int, co2: int, habitable_land: int
    ) -> None:
        self.bio_diversity = bio_diversity
        self.temperature = temperature
        self.co2 = co2
        self.habitable_land = habitable_land

    def __sign_helper(self, stat: int) -> str:
        if stat >= 0:
            return "+"
        else:
            return "-"

    def __str__(self) -> str:

        bio = __sign_helper(self.bio_diversity) + str(self.bio_diversity)
        temp = __sign_helper(self.temperature) + str(self.temperature)
        carbon = __sign_helper(self.co2) + str(self.co2)
        land = __sign_helper(self.habitable_land) + str(self.habitable_land)

        net_effects = (
            f"Biodiversity: {bio}\n"
            f"Temperature: {temp}\n"
            f"CO2: {carbon}\n"
            f"Habitable Land: {land}\n"
        )

        return net_effects
