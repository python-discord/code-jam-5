from __future__ import annotations

from typing import TYPE_CHECKING

from project.utils.singleton import Singleton

if TYPE_CHECKING:
    # Avoid cyclic imports
    # https://stackoverflow.com/a/39757388
    from .task import Task


class GameState(Singleton):
    """Class keeps variables and states related to the gameplay."""

    open_task: Task = None
    current_heat: float = 0
    is_playing: bool = False
