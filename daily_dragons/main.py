from game_modules.game import Game


def main():
    player_name = input("What is your name? ")
    game = Game(player_name)
    game.main()


if __name__ == "__main__":
    main()
