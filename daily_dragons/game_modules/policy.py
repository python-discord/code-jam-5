from .planetary_effects import PlanetaryEffects


class Policy:
    def __init__(
        self, name: str, description: str, planetary_effects: PlanetaryEffects
    ) -> None:
        self.name = name
        self.description = description
        self.planetary_effects = planetary_effects

    def __str__(self) -> str:
        output = f"{str(self.name)}\n{self.description}\n{str(self.planetary_effects)}"
        return output
