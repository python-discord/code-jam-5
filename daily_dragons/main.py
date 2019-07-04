from game_modules.start_menu import *


def main():
    window = pyglet.window.Window()
    gui = glooey.Gui(window)
    screen = glooey.VBox()
    bottom = glooey.HBox()

    bottom.add(glooey.Placeholder())
    bottom.add(glooey.Placeholder())

    screen.add(NamePrompt(), size=0)
    screen.add(NameForm(), size=0)
    screen.add(bottom, size='expand')
    gui.add(screen)

    pyglet.app.run()




if __name__ == "__main__":
    main()
