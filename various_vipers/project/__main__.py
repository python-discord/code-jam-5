"""
Python Discord Code Jam 5 - 2019.

"Various Vipers" team project
"""

import logging

from project.game import Game


logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Game launched. Have Fun!")

    game = Game()

    while game.running:
        game.run()
    quit()
