from typing import Dict
from colorama import Fore, Style
from .planet import Planet
from .player import Player
from .investment_options import InvestmentOptions


class Game:
    def __init__(self, name) -> None:
        self.player = Player(name)
        self.earth = Planet()
        self.investments = InvestmentOptions()

        self.quit_game = False
        self.round = 0

        help_options = (
            "stats: view current player stats",
            "earth: view current planet health",
            "invest [option]: invest in [option] company",
            "[option]: learn more about [option] company and their policies",
            "exit: quit the game",
        )
        self.help_menu = "\n".join(help_options)

        self.error_msg = Fore.RED + "Unrecognized input, try again or type help"

        self.exit_msg = (
            Fore.YELLOW + "Have a good day, thanks for playing!" + Style.RESET_ALL
        )

        self.fail_msg = (
            Fore.RED + "You have destroyed your planet. Enjoy the rest of your life "
            "knowing you've doomed humanity."
        )

        self.success_ending = (
            Fore.GREEN + "Congratuations! You've managed to save your world."
        )

        self.medium_ending = (
            Fore.YELLOW + "You managed to not destroy the world, but try better"
            " next time. You could have actually done some good "
            "in your life for once."
        )

        self.successful_order_msg = Fore.GREEN + "Ok, we've sent that in!"

        self.cancelled_order_msg = Fore.RED + "Ok, we'll cancel that order."

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
            # TODO: add rules / game explaination
            "select an option type 'invest [option]'. For more",
            "help, you can type 'help'.",
            "",
            "Good luck!",
            sep="\n",
        )

    def planet_stats_msg(self) -> str:
        planet_stats_msg = "\n".join(
            [
                Fore.GREEN + "Earth's current stats:" + Fore.WHITE,
                f"{self.earth.health_summary()}",
                f"{self.earth}",
            ]
        )

        return planet_stats_msg

    def player_stats_msg(self) -> str:
        player_stats_msg = f"Your current stats:\n{self.player}"
        return player_stats_msg

    def final_score(self) -> str:
        final_score = 0
        for stat in self.earth.stats.values():
            if stat >= 0:
                final_score += stat * 10000
            else:
                final_score += stat * 5000

        return f"Final score: {final_score}"

    def main(self) -> None:
        while not self.quit_game:
            if self.round >= 10:
                self.quit_game = True

                if sum(i >= 10 for i in self.earth.stats.values()) >= 2:
                    print(self.success_ending)
                else:
                    print(self.medium_ending)

                print(self.final_score())

            elif self.player.net_worth <= 0:
                print("You've run out of money.", self.exit_msg)

            elif not all(i > -10 for i in self.earth.stats.values()):
                self.quit_game = True
                print(self.fail_msg)

            else:
                print(
                    Fore.BLUE + f"Welcome to round {self.round}.",
                    self.investments,
                    sep="\n",
                )
                player_input = input(Style.RESET_ALL + "")
                response = self.parse_input(player_input)

                print(response, "\n\n")

    def _invest(self, option) -> str:
        try:
            chosen_investment = self.investments.options[option]
            print(chosen_investment)
            print("Investing in ", chosen_investment.organization.name)
            print("Are you sure? y/N")

            player_input = input("").casefold()

            if player_input == "y" or player_input == "yes":
                self.earth.affect_planet(
                    chosen_investment.current_policy.planetary_effects
                )
                self.player.get_roi(chosen_investment.current_policy.roi)
                chosen_investment.times_invested += 1
                print(self.successful_order_msg)
                return self.planet_stats_msg()
            else:
                return self.cancelled_order_msg

        except (KeyError, AttributeError):
            return self.error_msg

    def parse_input(self, token: str) -> Dict.values:

        input_options = {
            "help": self.help_menu,
            "exit": self.exit_msg,
            "stats": self.player_stats_msg(),
            "earth": self.planet_stats_msg(),
        }

        if token.isdigit():
            self.round += 1
            return self.investments.options.get(token, self.error_msg)
        elif token.casefold() == "exit":
            self.quit_game = True
            return input_options[token]
        elif len(token.split(" ")) < 2:
            return input_options.get(token, self.error_msg)
        else:
            args = token.split(" ")

            try:
                if args[0].casefold() == "invest":
                    self.round += 1
                    return self._invest(args[1])
                else:
                    return self.investments.options.get(args[1], self.error_msg)

            except ValueError:
                return self.error_msg
