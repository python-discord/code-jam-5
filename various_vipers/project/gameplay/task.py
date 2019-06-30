import logging
from typing import Optional

from .biome import Biome, BiomeCity, BiomeDesert, BiomeForest, BiomeMountains


logger = logging.getLogger(__name__)


class Task(object):
    """Generic class for game Task on earth."""

    def __init__(self, biome: Optional[Biome] = None):
        if isinstance(biome, BiomeCity):
            logger.debug(f"Generating city themed task of type {type(self)}")
        elif isinstance(biome, BiomeDesert):
            logger.debug(f"Generating desert themed task of type {type(self)}")
        elif isinstance(biome, BiomeForest):
            logger.debug(f"Generating forest themed task of type {type(self)}")
        elif isinstance(biome, BiomeMountains):
            logger.debug(f"Generating mountains themed task of type {type(self)}")


class TaskCursorMaze(Task):
    """
    Cursor Maze - players needs to move mouse cursor from point A to B without touching walls.

    Task should not take more than 10s to complete.
    Maze is generated automatically and is different each time.
    Task is themed around the biome this task spawned in.
    """

    pass


class TaskRockPaperScissors(Task):
    """
    Rock Paper Scissors - players gets a 1/3 chance to win the task.

    This task is fast and easy, rewarding lucky players.
    Task is themed around the biome this task spawned in.
    """

    pass


class TaskTicTacToe(Task):
    """
    Tic Tac Toe - players is playing a simple tic tac toe game against the computer.

    Task is themed around the biome this task spawned in.
    """

    pass
