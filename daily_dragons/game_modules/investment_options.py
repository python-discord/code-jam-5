# TODO convert to load from json
from .investment_placeholders import investments


class InvestmentOptions:
    def __init__(self):
        self.options = investments()
        self.option_names = []
        self.option_numbers = []
        for each_number, each_option in self.options.items():
            self.option_names.append(each_option.organization.name.casefold())
            self.option_numbers.append(each_number)

    def __str__(self):
        menu = []
        for key, i in self.options.items():
            menu.append(f"{key}: {i.organization.name}")
        return "\n".join(menu)
