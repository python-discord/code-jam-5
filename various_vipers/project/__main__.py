"""
Python Discord Code Jam 5 - 2019.

"Various Vipers" team project
"""

from project.game import Game

if __name__ == '__main__':
    game = Game()

    while game.running:
        game.run()
    quit()
