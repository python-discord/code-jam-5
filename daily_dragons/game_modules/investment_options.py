# TODO convert to load from json
from .investment_placeholders import investments


class InvestmentOptions:
    def __init__(self):
        self.options = investments()

    def __str__(self):
        menu = []
        for key, i in self.options.items():
            menu.append(f"{key}: {i.organization.name}")
        return "\n".join(menu)
