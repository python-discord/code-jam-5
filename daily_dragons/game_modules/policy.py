from .planetary_effects import PlanetaryEffects
from colorama import Fore


class Policy:
    """Policies are an organizations current goals, such as lobbying or
       changing laws to accomplish their goals. They can have positive
       or negative planetary effects and an ROI (return on investment)"""

    def __init__(
        self,
        name: str,
        description: str,
        planetary_effects: PlanetaryEffects,
        roi: float = 0.0,
    ) -> None:
        self.name = name
        self.description = description
        self.planetary_effects = planetary_effects
        self.roi = roi

    def __str__(self) -> str:
        output = (
            "" + Fore.CYAN + f"{str(self.name)}\n"
            "" + Fore.WHITE + f"{self.description}\n"
            f"{str(self.planetary_effects)}"
            "" + Fore.GREEN + "ROI:\t\t" + Fore.WHITE + f"{self.roi*100}%"
        )
        return output
