import datetime
import logging
import random
import time
from typing import List, Optional

import pygame as pg

from project.constants import Color, TILE_COLS, TILE_ROWS, WIDTH
from project.utils.helpers import realtime_to_ingame_formatted
from project.utils.user_data import UserData
from .biome import Biome, BiomeCity, BiomeDesert, BiomeForest, BiomeMountains
from .earth import Earth
from .game_state import GameState
from .sun import Sun
from .task import TaskCursorMaze, TaskRockPaperScissors, TaskTicTacToe


logger = logging.getLogger(__name__)
game_vars = GameState()
user_data = UserData()


class Period(object):
    """
    This class represents an abstract Time Period Style.

    Game difficulties are split into Time Periods - with each time period having different
      tile styles, tasks, images and chances to spawn cities.
    """

    # List of biomes, that will be looped through
    biomes: List[Biome]

    # Time passed after the last task spawn
    time_of_last_task_spawn: Optional[int] = None
    # How many game ticks between task spawns (will be floored and converted to int)
    task_spawn_freq: float = 420
    # Maximum frequency for task spawns
    task_spawn_freq_max: float = 30
    # How much to increase task spawn frequency with each game tick
    task_spawn_freq_inc: float = 0.05

    # How much heat goes up passively each game tick
    heat_per_tick: float = 0.005
    # How much heat goes up per task each game tick
    heat_per_task: float = 0.005

    # Chance to spawn certain task types
    maze_chance: float = 0
    rps_chance: float = 1.0
    ttt_chance: float = 0

    # Earth's age
    start_date: datetime = datetime.date(2000, 1, 1)
    # Time when game started
    start_time: time = None
    # Time when game ended
    end_time: time = None
    # Time when the game was last paused
    pause_time: time = None
    # Time how long the game was paused for
    pause_time_sum: float = 0

    def __init__(self, screen: pg.Surface):
        self.screen = screen

        self.biomes = [
            BiomeDesert(),
            BiomeDesert(),
            BiomeDesert(),
            BiomeMountains(),
            BiomeMountains(),
            BiomeMountains(),
            BiomeForest(),
            BiomeForest(),
            BiomeForest(),
            BiomeCity(),
            BiomeCity(),
            BiomeCity(),
        ]

        self.earth = Earth(self.screen, self.biomes)
        self.sun = Sun(
            self.screen, self.earth.biomes, self.heat_per_tick, self.heat_per_task
        )

    @property
    def hiscore(self) -> float:
        """Hiscore (seconds survived) for this game period."""
        if isinstance(self, PeriodMedieval):
            return user_data.hiscore_medieval
        elif isinstance(self, PeriodModern):
            return user_data.hiscore_modern
        elif isinstance(self, PeriodFuture):
            return user_data.hiscore_future

    @hiscore.setter
    def hiscore(self, new_hiscore: float) -> None:
        """Sets a new hiscore for this game period."""
        if isinstance(self, PeriodMedieval):
            user_data.hiscore_medieval = new_hiscore
        elif isinstance(self, PeriodModern):
            user_data.hiscore_modern = new_hiscore
        elif isinstance(self, PeriodFuture):
            user_data.hiscore_future = new_hiscore

    @property
    def elapsed(self) -> None:
        """Returns time elapsed in seconds from the game start (ignore pause time)."""
        if self.end_time is not None:
            return self.end_time - self.start_time - self.pause_time_sum
        return time.time() - self.start_time - self.pause_time_sum

    def update(self, event: pg.event) -> None:
        """Update gets called every game tick."""
        self.earth.update(event)
        self.sun.update(event)

        if game_vars.is_started:
            self.end_time = None
            if self.start_time is None:
                self.start_time = time.time()
            self.__handle_task_spawn()
        elif self.end_time is None:
            self.end_time = time.time()

    def draw(self) -> None:
        """Draw gets called every game tick."""
        self.screen.fill(Color.sky)
        self.earth.draw(self.sun)
        self.draw_age()

    def draw_age(self) -> None:
        """Draw how long the earth lived."""
        if self.start_time is not None:
            if game_vars.is_paused:
                if not self.pause_time:
                    self.pause_time = time.time()
                self.pause_time_sum = time.time() - self.pause_time
            else:
                self.pause_time = None
            font = pg.font.Font(None, 50)
            text = realtime_to_ingame_formatted(self.elapsed, self.start_date)
            age_indicator = font.render(text, True, pg.Color("black"))
            self.screen.blit(
                age_indicator,
                (int(WIDTH // 2) - int(age_indicator.get_width() // 2), 0),
            )

    def __handle_task_spawn(self) -> None:
        if (
            self.time_of_last_task_spawn is None
            or self.time_of_last_task_spawn >= self.task_spawn_freq
        ):
            self.time_of_last_task_spawn = 0
            self.__spawn_task()
        else:
            self.time_of_last_task_spawn += 1
        self.task_spawn_freq = self.task_spawn_freq - self.task_spawn_freq_inc
        self.task_spawn_freq = max(self.task_spawn_freq, self.task_spawn_freq_max)

    def __spawn_task(self) -> None:
        """Spawns a task on a random tile."""
        # TODO :: add check if tile already has a task or not.
        # Get number of tiles between all biomes
        tile_count = TILE_COLS * TILE_ROWS * len(self.biomes)
        # Chose a random tile out of all
        random_tile_idx = random.randint(0, tile_count - 1)
        # Calculate biome index from the global tile index
        biome_idx = random_tile_idx // (TILE_COLS * TILE_ROWS)
        # Calculate tile index local to the biome chosen
        tile_in_biome_idx = random_tile_idx - (TILE_COLS * TILE_ROWS * biome_idx)
        tile_y = tile_in_biome_idx // TILE_COLS
        tile_x = tile_in_biome_idx - (tile_y * TILE_COLS)

        biome = self.biomes[biome_idx]
        tile = biome.tilemap[tile_y][tile_x]
        new_task = random.choices(
            [TaskCursorMaze, TaskRockPaperScissors, TaskTicTacToe],
            weights=[self.maze_chance, self.rps_chance, self.ttt_chance],
        )
        tile.task = new_task[0](self.screen, biome)

        self.earth.fix_indicators()


class PeriodMedieval(Period):
    """Medieval themed Time Period."""

    start_date: datetime = datetime.date(1000, 1, 1)


class PeriodModern(Period):
    """Modern time themed Time Period."""

    start_date: datetime = datetime.date(2000, 1, 1)


class PeriodFuture(Period):
    """Future time themed Time Period."""

    start_date: datetime = datetime.date(3000, 1, 1)
