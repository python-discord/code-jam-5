from game_modules.game import Game
from colorama import Fore
import pyfiglet

if __name__ == "__main__":
    print(pyfiglet.figlet_format("Who wants to be a Billionare?"))
    player_name = input(Fore.RED + "What is your name? " + Fore.WHITE)
    game = Game(player_name)
    game.main()
