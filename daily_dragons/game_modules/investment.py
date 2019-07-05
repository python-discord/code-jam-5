from typing import List
from .news import News
from .organization import Organization
from .policy import Policy


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
        policies: List[Policy],
        news_on_apperance: List[News] = None,
        news_on_investment: List[News] = None,
        news_on_no_investment: List[News] = None,
    ) -> None:
        self.organization = organization
        self.policies = policies
        self.news_on_apperance = news_on_apperance
        self.news_on_investment = news_on_investment
        self.news_on_no_investment = news_on_no_investment
        self.times_invested = 0

    def __str__(self) -> str:
        output = f"{str(self.organization)}\n{str(self.current_policy)}"
        return output

    @property
    def current_policy(self) -> (Policy, None):
        if self.policies:
            return self.policies[self.times_invested]
        else:
            return None
