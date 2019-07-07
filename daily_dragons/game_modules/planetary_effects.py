from colorama import Fore


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
        `temperature` is the change in C (celsius)
        `co2` is tracked in ppm (parts per million)
        `habitable_land` is in hectares (100 acres)
        """
        self.bio_diversity = bio_diversity
        self.temperature = temperature
        self.co2 = co2
        self.habitable_land = habitable_land

    def __sign_helper(self, stat: int) -> str:
        if stat > 0:
            return "+"
        elif stat < 0:
            return ""
        else:
            return " "

    def __level_helper(self, stat: int) -> str:
        if stat == 0:
            return " -"
        elif stat == 1:
            return f"{self.__sign_helper(stat)}{str(stat)} level"
        else:
            return f"{self.__sign_helper(stat)}{str(stat)} levels"

    def __str__(self) -> str:

        bio = self.__level_helper(self.bio_diversity)
        temp = self.__level_helper(self.temperature)
        carbon = self.__level_helper(self.co2)
        land = self.__level_helper(self.habitable_land)

        net_effects = (
            "" + Fore.GREEN + f"Biodiversity:\t" + Fore.WHITE + f"{bio}\n"
            "" + Fore.GREEN + f"Temperature:\t" + Fore.WHITE + f"{temp}\n"
            "" + Fore.GREEN + f"CO2:\t\t" + Fore.WHITE + f"{carbon}\n"
            "" + Fore.GREEN + f"Habitable Land:\t" + Fore.WHITE + f"{land}\n"
        )

        return net_effects
