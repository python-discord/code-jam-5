from planet import Planet
from player import Player
from company import Company
from planetary_effects import PlanetaryEffects


def main():
    earth = Planet()
    player_name = input("What is your name? ")
    player = Player(player_name)

    print(f"Hello, {player_name}")
    print(player)
    print("Current Earth Stats:")
    print(earth)

    bad_effects = PlanetaryEffects(-100, -0.02, 20, -100)
    evil_corp = Company(
        "Faux News",
        (
            "Evil news corp that spreads lies and misinformation"
            " to benifit companies for the sake of profit"
        ),
        bad_effects,
        0.20,
    )

    print(evil_corp)


if __name__ == "__main__":
    main()
