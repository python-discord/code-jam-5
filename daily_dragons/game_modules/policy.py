from .planetary_effects import PlanetaryEffects


class Policy:
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
        output = f"{str(self.name)}\n{self.description}\n{str(self.planetary_effects)}"
        return output
