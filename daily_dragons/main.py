from planet import Planet
from player import Player


def main():
    earth = Planet()
    player_name = input("What is your name? ")
    player = Player(player_name)

    print(f"Hello, {player_name}")
    print(player)
    print("Current Earth Stats:")
    print(earth)


if __name__ == "__main__":
    main()
