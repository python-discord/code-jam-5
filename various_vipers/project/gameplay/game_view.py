import logging

from .period import PeriodFuture, PeriodMedieval, PeriodModern


logger = logging.getLogger(__name__)


class GameView:
    """GameView hold the information about all things related to the main game."""

    # Background images that will be looping
    BG_images = []

    def __init__(self, screen, difficulty=0):
        """
        screen - parent screen to draw objects on
        difficulty - 0, 1, 2. Difficulty increases with number.
        """
        self.screen = screen

        if difficulty == 0:
            self.period = PeriodMedieval(self.screen)
        elif difficulty == 1:
            self.period = PeriodModern(self.screen)
        elif difficulty == 2:
            self.period = PeriodFuture(self.screen)
        else:
            raise Exception(f"Unknown difficulty level passed: {difficulty}")

    def update(self):
        self.period.update()

    def draw(self):
        self.period.draw()
