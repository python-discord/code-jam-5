from planetary_effects import PlanetaryEffects


class Organization:
    def __init__(
        self, name: str, description: str, planetary_effects: PlanetaryEffects
    ) -> None:
        self.name = name
        self.description = description
        self.planetary_effects = planetary_effects

    def __str__(self) -> str:
        summary = f"{self.name}\n" f"{self.description}\n" f"Bio Diversity:"
        return summary
