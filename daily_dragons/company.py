from organization import Organization
from planetary_effects import PlanetaryEffects


class Company(Organization):
    """
    Company extends Organization

    A company, unlike an NGO, has a return on investiment (roi)
    that increases the player's net worth when invested into

    """

    def __init__(
        self, name: str, description: str, planetary_effects: PlanetaryEffects, roi: int
    ) -> None:
        """
        """
        super().__init__(name, description, planetary_effects)
        self.roi = 0
