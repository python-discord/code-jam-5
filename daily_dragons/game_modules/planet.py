from typing import Dict
from .planetary_effects import PlanetaryEffects
from colorama import Fore


class Planet:
    """Track the planets health with key statistics"""

    def __init__(
        self,
        bio_diversity: int = 0,
        temperature: int = 0,
        co2: int = 0,
        habitable_land: int = 0,
    ) -> None:
        """
        Track the stats as a net change from baseline

        bio diversity tracks the change in the total number of species
        temperature is the change in C (celsius)
        co2 is tracked in ppm (parts per million)
        habitable land is in hectacres (100 acres)
        """
        self.stats = {
            "bio_diversity": bio_diversity,
            "temperature": temperature,
            "co2": co2,
            "habitable_land": habitable_land,
        }

    def _get_seperate_stats(self):
        bio_div = self.stats.get("bio_diversity", "That wasn't here. Please restart the game.")
        temperature = self.stats.get("temperature", "That wasn't here. Please restart the game.")
        co2 = self.stats.get("co2", "That wasn't here. Please restart the game.")
        land = self.stats.get("habitable_land", "That wasn't here. Please restart the game.")

        return bio_div, temperature, co2, land

    @property
    def scoreboard(self) -> Dict[str, str]:
        """A dict of the stats for easy output by gui"""
        bio_div, temperature, co2, land = self._get_seperate_stats()
        current_stats = (
            Fore.GREEN
            + f"Biodiversity:\t"
            + Fore.WHITE
            + f"{bio_div} species\n"
            + Fore.GREEN
            + f"Temperature:\t"
            + Fore.WHITE
            + f"{temperature} C\n"
            + Fore.GREEN
            + f"CO2:\t\t"
            + Fore.WHITE
            + f"{co2} ppm\n"
            + Fore.GREEN
            + f"Habitable Land:\t"
            + Fore.WHITE
            + f"{land} hectacres \n"
        )

        return current_stats

    def affect_planet(self, effects: PlanetaryEffects) -> None:
        """Applies the changes of an effect in place to the planet"""
        self.stats["bio_diversity"] += effects.bio_diversity
        self.stats["temperature"] += effects.temperature
        self.stats["co2"] += effects.co2
        self.stats["habitable_land"] += effects.habitable_land

    def health_summary(self) -> str:
        """Provides a human readable summary of the health on the planet based on its stats"""
        health = []

        bio_div, temperature, co2, land = self._get_seperate_stats()

        # Estimates have us around 9 million species
        # Extinction events appear to be ~75% of all species dying
        if bio_div >= 10:
            health.append("Species have returned en masse and the ecosystem is doung wonderfully.")
        elif bio_div >= 5:
            health.append("Species thought to be extinct are beginning to return.")
        elif bio_div >= -5:
            health.append("There has been no noticeable change in the number of species.")
        elif bio_div > -10:
            health.append("Species are dying en masse.")
        else:
            health.append("A mass extinction event has occurred.")

        if temperature >= 10:
            health.append("Temperatures have been brought down to healthy levels, the ice caps have"
                          " refrozen.")
        elif temperature >= 5:
            health.append("The ice caps are beginning to regrow.")
        elif temperature >= -5:
            health.append("There has been no noticeable change in the temperature or ice caps.")
        elif temperature > -10:
            health.append("The ice caps are beginning to shrink.")
        else:
            health.append("The ice caps have completely shrunk, and the world is now unbearably "
                          "hot.")

        return " ".join(health)

    def __str__(self) -> str:
        status_messages = []
        for stat in self._get_seperate_stats():
            if stat > 10:
                status_messages.append("You have caused a saved this stat.")
            elif stat > 5:
                status_messages.append("You have caused a major net gain.")
            elif stat > 0:
                status_messages.append("You have caused a net gain.")
            elif stat > 5:
                status_messages.append("You have caused a net loss.")
            elif stat > 10:
                status_messages.append("You have caused a major net loss.")
            else:
                status_messages.append("You have ruined this beyond the point of return. You've "
                                       "destroyed the world.")

        current_stats = (
            f"bio_diversity: {status_messages[0]} \n"
            f"temperature: {status_messages[1]} \n"
            f"co2: {status_messages[2]} \n"
            f"habitable_land: {status_messages[3]} \n"
        )

        return current_stats
