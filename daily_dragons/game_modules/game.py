from typing import Dict

from .planet import Planet
from .player import Player
from .investment_options import InvestmentOptions


class Game:
    def __init__(self, name) -> None:
        self.quit_game = False

        self.input_options = {
            "help": self.help_menu,
            "exit": self.leave_game,
            "stats": self.player_stats,
            "earth": self.planet_stats,
        }

        self.player = Player(name)
        self.earth = Planet()
        self.investments = InvestmentOptions()

        print(
            f"Hello {name},",
            "Congratulations on your inheritance. I'm sorry to",
            "hear about your grandpa passing though.",
            "",
            "Regardless, you now find yourself in a position to",
            "enact the change you've always wanted to. Each",
            "financial period, you will be responsible for",
            "investing in your choice of various groups. Each",
            "will have an impact on your planet.",
            "",
            "You can view the effects a certain option will",
            "have by typing the name or number of it. To",
            # TODO: change instructions for gui if/when implemented
            "select an option type 'invest [option]'. For more",
            "help, you can type 'help'.",
            "",
            "Good luck!",
            sep="\n",
        )

    def main(self) -> None:
        while not self.quit_game:
            print(self.investments)
            player_input = input("")

            response = self.parse_input(player_input)

            print(response())

    @staticmethod
    def help_menu() -> str:
        menu = (
            "stats: view current player stats",
            "earth: view current planet health",
            "invest: choose an investment",
            "exit: quit the game",
        )

        return "\n".join(menu)

    def player_stats(self) -> str:
        output = f"Your current stats:\n{self.player}"
        return output

    def planet_stats(self) -> str:
        output = f"Earth's current stats:\n{self.earth.health_summary()}\n{self.earth}"

        return output

    def leave_game(self) -> str:
        self.quit_game = True
        return "Have a good day, thanks for playing!"

    def error(self) -> str:
        return "Unrecognized input, try again or type help"

    def successful_order(self) -> str:
        return "Ok, we've sent that in!"

    def cancelled_order(self) -> str:
        return "Ok, we'll cancel that order."

    def _invest(self, option) -> None:
        try:
            chosen_investment = self.investments.options[option]
            print(chosen_investment)
            print("Investing in ", chosen_investment.organization.name)
            print("Are you sure? Y/N")

            player_input = input("")

            if player_input.lower() == "y" or player_input.lower() == "yes":
                self.earth.affect_planet(chosen_investment.planetary_effects)
                return self.successful_order
            else:
                return self.cancelled_order

        except (KeyError, AttributeError):
            return self.error

    def parse_input(self, token: str) -> Dict.values:
        if len(token.split(" ")) < 2:
            return self.input_options.get(token, self.error)
        else:
            args = token.split(" ")
            choice = args[1]
            return self._invest(choice)
