from typing import List
from news import News
from organization import Organization
from planetary_effects import PlanetaryEffects


class Investment:
    """
    Investments are choices presented to the player on how they
    allocate their money. Investements will have a positive, negative
    or possiblely no affect on the planet and could generate news, ROI funds
    or unlock new investment opportunities in future rounds.
    """

    def __init__(
        self,
        organization: Organization,
        planetary_effects: PlanetaryEffects,
        news_on_apperance: List[News],
        news_on_investment: List[News],
        news_on_no_investment: List[News],
        roi: int = 0,
    ) -> None:
        self.organization = organization
        self.planetary_effects = planetary_effects
        self.news_on_apperance = news_on_apperance
        self.news_on_investment = news_on_investment
        self.news_on_no_investment = news_on_no_investment
        self.roi = roi
