"""
Python Discord Code Jam 5 - 2019.

"Various Vipers" team project
"""

import logging
import sys

from project.game import Game


logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Game launched. Have Fun!")

    # Temp fix to go straight to the game
    if len(sys.argv) > 1:
        game = Game(True)
    else:
        game = Game()

    while game.running:
        game.run()
    quit()
