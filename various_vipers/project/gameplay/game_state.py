from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from project.utils.singleton import Singleton
from project.utils.user_data import UserData

if TYPE_CHECKING:
    # Avoid cyclic imports
    # https://stackoverflow.com/a/39757388
    from .task import Task
    from .period import Period


logger = logging.getLogger(__name__)
user_data = UserData()


class GameState(Singleton):
    """Class keeps variables and states related to the gameplay."""

    open_task: Task = None
    current_heat: float = 0
    is_started: bool = False
    is_paused: bool = False

    # Set this when the game should be reset
    # Will be watched from Game class
    reset_game: bool = False

    def reset(self, period: Period) -> None:
        """Reset game state - called when game ends."""
        self.save_score(period)

        self.open_task = None
        self.current_heat = 0
        self.is_started = False
        self.is_paused = False
        self.reset_game = False

    def save_score(self, period: Period) -> None:
        """Save current score for this period."""
        from .period import PeriodFuture, PeriodMedieval, PeriodModern

        if isinstance(period, PeriodMedieval):
            user_data.hiscore_medieval = max(period.elapsed, user_data.hiscore_medieval)
        elif isinstance(period, PeriodModern):
            user_data.hiscore_modern = max(period.elapsed, user_data.hiscore_modern)
        elif isinstance(period, PeriodFuture):
            user_data.hiscore_future = max(period.elapsed, user_data.hiscore_future)

        logger.debug(f"Saving score... {period.elapsed:.2f}s survived")
        user_data.save()
