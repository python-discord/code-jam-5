import logging
from dataclasses import dataclass
from enum import Enum
from random import choice
from time import time
from typing import List, Optional, Tuple

import pygame as pg

from project.constants import Color, HEIGHT, WIDTH
from .game_state import GameState
from .biome import Biome, BiomeCity, BiomeDesert, BiomeForest, BiomeMountains


logger = logging.getLogger(__name__)
game_vars = GameState()


class Task(object):
    """Generic class for game Task on earth."""

    # Marked when task is completed or closed, so it can be deleted
    is_done: bool = False
    # Time when task started
    time_start: Optional[time] = None
    # Time limit in seconds until the task closes
    time_limit: float = 10

    # How much heat does success/failure add
    heat_add_success: float = 0
    heat_add_failure: float = 0

    def __init__(self, screen: pg.Surface, biome: Optional[Biome] = None):
        self.screen = screen

        self.window_rect = pg.Rect(
            int(WIDTH * 0.1), int(HEIGHT * 0.1), int(WIDTH * 0.8), int(HEIGHT * 0.8)
        )

        if isinstance(biome, BiomeCity):
            logger.debug(f"Generating city themed task of type {type(self)}")
        elif isinstance(biome, BiomeDesert):
            logger.debug(f"Generating desert themed task of type {type(self)}")
        elif isinstance(biome, BiomeForest):
            logger.debug(f"Generating forest themed task of type {type(self)}")
        elif isinstance(biome, BiomeMountains):
            logger.debug(f"Generating mountains themed task of type {type(self)}")

    @property
    def _time_left(self) -> float:
        """Returns time left on this task."""
        if self.time_start:
            return max(self.time_limit - (time() - self.time_start), 0)
        return self.time_limit

    def start(self, start_timer: bool = True) -> None:
        """Start playing the task."""
        game_vars.open_task = self
        if start_timer:
            self.time_start = time()

    def update(self) -> None:
        """Update is called every game tick."""
        if self.time_start and self._time_left <= 0:
            self._complete(False)

    def draw(self) -> None:
        """Draw is called every game tick."""
        self.screen.fill(Color.black, self.window_rect)
        if self.time_start:
            self._draw_timer()

    def _complete(self, successful: bool) -> None:
        """Called when task was completed."""
        logger.debug(successful)
        game_vars.open_task = None
        game_vars.current_heat += (
            self.heat_add_success if successful else self.heat_add_failure
        )
        self.is_done = True

    def _draw_timer(self) -> None:
        font = pg.font.Font(None, 70)
        time_left = self._time_left
        timer = font.render(f"{time_left:.2f}s", True, pg.Color("red"))
        timer_x = self.window_rect.x + self.window_rect.width - timer.get_width()
        timer_y = self.window_rect.y - 45
        self.screen.blit(timer, (timer_x, timer_y))


class TaskCursorMaze(Task):
    """
    Cursor Maze - players needs to move mouse cursor from point A to B without touching walls.

    Task should not take more than 10s to complete.
    Maze is generated automatically and is different each time.
    Task is themed around the biome this task spawned in.
    """

    # How much heat does success/failure add
    heat_add_success: float = -5
    heat_add_failure: float = 0

    maze: List["Cell"]

    maze_start: Tuple[int, int] = (5, 7)  # Y, X
    # width and height include the border of the maze
    maze_width: int = 15
    maze_height: int = 11

    # If the player has started the maze - moved mouse over start
    started: bool = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cell_size = (
            self.window_rect.width // self.maze_width,
            self.window_rect.height // self.maze_height,
        )

    def start(self) -> None:
        """Generate the maze when user clicks on task."""
        super().start()
        self.__generate_maze()

    def update(self, event: pg.event) -> None:
        """Check mouse collisions if player is in maze."""
        super().update()

        for cell in self.maze:
            mouse_hover = cell.rect.collidepoint(pg.mouse.get_pos())
            if (
                not self.started
                and cell.cell_type == self.CellType.START
                and mouse_hover
            ):
                self.started = True
            elif self.started and mouse_hover:
                if cell.cell_type == self.CellType.END:
                    self._complete(True)
                elif cell.cell_type == self.CellType.WALL:
                    self._complete(False)

    def draw(self) -> None:
        """Draw the maze."""
        super().draw()

        # Draw the maze
        for cell in self.maze:
            # Only draw the starting cell if player has not started the maze
            if self.started or cell.cell_type == self.CellType.START:
                self.screen.fill(cell.color, cell.rect)

    def __generate_maze(self) -> None:
        """
        Generates a maze for this task.

        Depth-first search algorithm is used.
        Algorithm recursively navigates through nodes
          and marks then as visited or wall depending if it has visited neighbors.
        We are keeping track of longest path from start that will be set as maze solution.
        """
        # farthest point from starting point
        self.maze = []
        farthest = (0, None)
        row = (
            [self.CellType.WALL]
            + ([self.CellType.UNVISITED] * (self.maze_width - 2))
            + [self.CellType.WALL]
        )
        cells = (
            [[self.CellType.WALL] * (self.maze_width)]
            + [row[:] for _ in range(self.maze_height - 2)]
            + [[self.CellType.WALL] * (self.maze_width)]
        )

        def deeper(prev_y: int, prev_x: int, new_y: int, new_x: int, n: int = 0):
            """
            Recursively navigate through maze map.

            prev_y, prev_x -> where we came from
            new_y, new_x -> position to investigate now
            n -> current path length
            """
            if cells[new_y][new_x] != self.CellType.UNVISITED:
                return

            # Create a list of possible nodes to visit
            directions = []
            if new_x > 0 and (new_y, new_x - 1) != (prev_y, prev_x):
                directions.append((new_y, new_x - 1))
            if new_x < self.maze_width - 1 and (new_y, new_x + 1) != (prev_y, prev_x):
                directions.append((new_y, new_x + 1))
            if new_y > 0 and (new_y - 1, new_x) != (prev_y, prev_x):
                directions.append((new_y - 1, new_x))
            if new_y < self.maze_height - 1 and (new_y + 1, new_x) != (prev_y, prev_x):
                directions.append((new_y + 1, new_x))

            # Check if any possible visit node was visited.
            # We don't want to have 2 visited nodes together, unless it is where we came from.
            for direction in directions:
                if cells[direction[0]][direction[1]] == self.CellType.VISITED:
                    cells[new_y][new_x] = self.CellType.WALL
                    return

            cells[new_y][new_x] = self.CellType.VISITED

            # Increment current path length; check if it is the longest path.
            n += 1
            nonlocal farthest
            if n > farthest[0]:
                farthest = (n, (new_y, new_x))

            # Try all the possible nodes
            while len(directions) > 0:
                direction = choice(directions)
                if direction:
                    deeper(new_y, new_x, *direction, n)
                    directions.remove(direction)

        # Start generating the maze
        deeper(None, None, *self.maze_start)
        # Mark starting and ending nodes
        cells[self.maze_start[0]][self.maze_start[1]] = self.CellType.START
        cells[farthest[1][0]][farthest[1][1]] = self.CellType.END

        # Convert 2D array of CellType to 1D array of Cell
        y = self.window_rect.y
        for row in cells:
            x = self.window_rect.x
            for cell in row:
                rect = pg.Rect(x, y, *self.cell_size)
                color = Color.white
                if cell == self.CellType.WALL:
                    color = Color.black
                elif cell == self.CellType.START:
                    color = Color.green
                elif cell == self.CellType.END:
                    color = Color.red
                self.maze.append(self.Cell(rect, color, cell))

                x += self.cell_size[0]
            y += self.cell_size[1]

    @dataclass
    class Cell:
        """Maze cell object class."""

        rect: pg.Rect
        color: Color
        cell_type: "CellType"  # noqa

    class CellType(Enum):
        """Type of cell in maze map."""

        UNVISITED = 1
        VISITED = 2
        WALL = 3
        START = 4
        END = 5


class TaskRockPaperScissors(Task):
    """
    Rock Paper Scissors - players gets a 1/3 chance to win the task.

    This task is fast and easy, rewarding lucky players.
    Task is themed around the biome this task spawned in.
    """

    # How much heat does success/failure add
    heat_add_success: float = 0
    heat_add_failure: float = 0

    def start(self) -> None:
        super().start()

    def update(self, event: pg.event) -> None:
        super().update()

    def draw(self) -> None:
        super().draw()


class TaskTicTacToe(Task):
    """
    Tic Tac Toe - players is playing a simple tic tac toe game against the computer.

    Task is themed around the biome this task spawned in.
    """

    # How much heat does success/failure add
    heat_add_success: float = 0
    heat_add_failure: float = 0

    def start(self) -> None:
        super().start()

    def update(self, event: pg.event) -> None:
        super().update()

    def draw(self) -> None:
        super().draw()
