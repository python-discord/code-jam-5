from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Avoid cyclic imports
    # https://stackoverflow.com/a/39757388
    from .task import Task


open_task: Task = None


def set_open_task(task: Task) -> None:
    """Sets currently open task."""
    global open_task
    open_task = task


def get_open_task() -> Task:
    """Return currently open task."""
    return open_task
