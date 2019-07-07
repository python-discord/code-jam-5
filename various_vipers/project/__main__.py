"""
Python Discord Code Jam 5 - 2019.

"Various Vipers" team project
"""

import logging

from project.constants import PROFILING
from project.game import Game


logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("Game launched. Have Fun!")

    game = Game()

    # Check if we want to profile the game
    # This will enable and start gathering information
    #   about function calls, time it takes to run them, etc.
    if PROFILING:
        import cProfile
        import pstats
        import io
        from pstats import SortKey

        pr = cProfile.Profile()
        pr.enable()

    while game.running:
        game.run()

    # End profiling and print results
    if PROFILING:
        pr.disable()
        p_stream = io.StringIO()
        ps = pstats.Stats(pr, stream=p_stream).sort_stats(SortKey.CUMULATIVE)
        ps.print_stats()
        logger.debug(p_stream.getvalue())
