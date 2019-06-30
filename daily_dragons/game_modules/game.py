from typing import Dict

from .planet import Planet
from .player import Player
from .investment_options import InvestmentOptions


class Game:
    def __init__(self, name):
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

    def main(self):
        while not self.quit_game:
            print(self.investments)
            player_input = input("")

            response = self.parse_input(player_input)

            print(response())

    @staticmethod
    def help_menu():
        menu = (
            "stats: view current player stats",
            "earth: view current planet health",
            "invest: choose an investment",
            "exit: quit the game",
        )

        return "\n".join(menu)

    def player_stats(self):
        print("Your current stats:")
        print(self.player)

    def planet_stats(self):
        print("Earth's current stats:")
        print(self.earth.health_summary())
        print(self.earth)

    def leave_game(self):
        self.quit_game = True
        return "Have a good day, thanks for playing!"

    def invest(self):
        print("Who did you want to invest in?")
        print(self.investments)
        player_input = input("")

        self._invest(player_input)

    def _invest(self, option):
        try:
            chosen_investment = self.investments.get(option)
            print("Investing in ", chosen_investment.organization.name)
            print("Are you sure? Y/n")

            player_input = input("")

            if player_input == "n" or player_input == "no":
                print("Ok, we'll cancel that order.")
            else:
                print("Ok, we've sent that in!")
                self.earth.affect_planet(chosen_investment.planetary_effects)

        except AttributeError:
            print("Unrecognized input, try again or type help")

    def parse_input(self, token: str) -> Dict.values:

        if len(token.split(" ")) < 2:
            return self.input_options[token]
        else:
            args = token.split(" ")
            choice = " ".join(args[1:])
            self._invest(choice)
