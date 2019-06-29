from planet import Planet


def main():
    earth = Planet()
    player_name = input("What is your name? ")
    print(f"Hello, {player_name}")
    print("Current Earth Stats:")
    print(earth)


if __name__ == "__main__":
    main()
