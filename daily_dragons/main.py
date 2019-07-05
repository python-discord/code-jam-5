from game_modules.game import Game


if __name__ == "__main__":
    player_name = input("What is your name? ")
    game = Game(player_name)
    game.main()
