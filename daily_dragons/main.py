from game_modules.game import Game
from colorama import Fore

if __name__ == "__main__":
    player_name = input(Fore.RED + "What is your name? " + Fore.WHITE)
    game = Game(player_name)
    game.main()
