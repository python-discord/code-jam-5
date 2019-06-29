class PlanetaryEffects:
    """
    PlanetaryEffects

    Helper class for changing the affects player decisions have on the planet
    """

    def __init__(
        self, bio_diversity: int, temperature: int, co2: int, habitable_land: int
    ) -> None:
        """Track the stats as a direct change to the planets current stats

        `bio_diversity` tracks the change in the total number of species
        `tempature` is the change in C (celsius)
        `co2` is tracked in ppm (parts per million)
        `habitable_land` is in hectacres (100 acres)
        """
        self.bio_diversity = bio_diversity
        self.temperature = temperature
        self.co2 = co2
        self.habitable_land = habitable_land

    def __sign_helper(self, stat: int) -> str:
        if stat >= 0:
            return "+"
        else:
            return ""

    def __str__(self) -> str:

        bio = self.__sign_helper(self.bio_diversity) + str(self.bio_diversity)
        temp = self.__sign_helper(self.temperature) + str(self.temperature)
        carbon = self.__sign_helper(self.co2) + str(self.co2)
        land = self.__sign_helper(self.habitable_land) + str(self.habitable_land)

        net_effects = (
            f"Biodiversity: {bio}\n species"
            f"Temperature: {temp}\n C"
            f"CO2: {carbon}\n ppm"
            f"Habitable Land: {land}\n hectacres"
        )

        return net_effects
