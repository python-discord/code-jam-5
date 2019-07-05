import pyglet
from game_modules.start_menu import make_gui
from game_modules.game import Game


def run_gui() -> None:
    pyglet.resource.path = ["resources"]
    pyglet.resource.reindex()

    start_window = pyglet.window.Window()

    gui = make_gui(start_window)

    pyglet.app.run()


if __name__ == "__main__":
    player_name = input("What is your name? ")
    if player_name == "gui":
        run_gui()
    else:
        game = Game(player_name)
        game.main()
