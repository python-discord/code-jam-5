import logging
from typing import Optional

import pygame as pg
from pygame.image import load

from project.UI.element.button import Button
from project.constants import BUTTONS, Color, HEIGHT, WIDTH
from . import set_open_task
from .biome import Biome, BiomeCity, BiomeDesert, BiomeForest, BiomeMountains


logger = logging.getLogger(__name__)


class Task(object):
    """Generic class for game Task on earth."""

    # Marked when task is completed or closed, so it can be deleted
    is_done: bool = False

    hover_close: bool = False

    def __init__(self, screen: pg.Surface, biome: Optional[Biome] = None):
        self.screen = screen

        self.fill_rect = pg.Rect(
            int(WIDTH * 0.1), int(HEIGHT * 0.1), int(WIDTH * 0.8), int(HEIGHT * 0.8)
        )

        button_size = 60
        self.close_btn = Button(
            self.screen,
            x=self.fill_rect.x + self.fill_rect.width - button_size - 5,
            y=self.fill_rect.y + 5,
            width=button_size,
            height=button_size,
            image=load(str(BUTTONS["close-btn"])).convert_alpha(),
            image_hover=load(str(BUTTONS["close-btn-hover"])).convert_alpha(),
        )

        if isinstance(biome, BiomeCity):
            logger.debug(f"Generating city themed task of type {type(self)}")
        elif isinstance(biome, BiomeDesert):
            logger.debug(f"Generating desert themed task of type {type(self)}")
        elif isinstance(biome, BiomeForest):
            logger.debug(f"Generating forest themed task of type {type(self)}")
        elif isinstance(biome, BiomeMountains):
            logger.debug(f"Generating mountains themed task of type {type(self)}")

    def start(self) -> None:
        """Start playing the task."""
        set_open_task(self)
        logger.debug("Starting task.")

    def update(self, event: pg.event) -> None:
        """Update is called every game tick."""
        if self.close_btn.rect.collidepoint(pg.mouse.get_pos()):
            self.hover_close = True
            if event.type == pg.MOUSEBUTTONDOWN:
                set_open_task(None)
                self.is_done = True
        else:
            self.hover_close = False

    def draw(self) -> None:
        """Draw is called every game tick."""
        self.screen.fill(Color.black, self.fill_rect)
        self.close_btn.draw(hover=self.hover_close)


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
