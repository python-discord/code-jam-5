from typing import List
from .organization import Organization
from .policy import Policy


class Investment:
    """
    Investments are choices presented to the player on how they
    allocate their money. Investements will have a positive, negative
    or possiblely no affect on the planet and could generate ROI funds
    or unlock new investment opportunities in future rounds.
    """

    def __init__(self, organization: Organization, policies: List[Policy]) -> None:
        self.organization = organization
        self.policies = policies
        self.times_invested = 0

    def __str__(self) -> str:
        if self.current_policy:
            output = f"{str(self.organization)}\n{str(self.current_policy)}"
        else:
            output = f"{str(self.organization)}\nNo remaining policies"
        return output

    @property
    def current_policy(self) -> (Policy, None):
        if self.policies and self.times_invested < len(self.policies):
            return self.policies[self.times_invested]
        else:
            return None
