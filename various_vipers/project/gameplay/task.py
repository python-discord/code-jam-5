import logging
from dataclasses import dataclass
from enum import Enum
from random import choice, randint, shuffle
from time import time
from typing import List, Optional, Tuple

import pygame as pg
from pygame.image import load
from pygame.transform import scale

from project.UI.fx.sound import Sound
from project.constants import (
    Color,
    HEIGHT,
    MAZE_END,
    MAZE_PATH,
    MAZE_START,
    MAZE_WALL,
    O,
    PAPER,
    QUESTION_MARK,
    ROCK,
    SCISSORS,
    TTT_GRID,
    WIDTH,
    X,
)
from project.utils.notification import Notification
from .game_state import GameState


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

    def __init__(self, screen: pg.Surface, biome: Optional["Biome"] = None):
        self.screen = screen
        self.biome = biome

        self.window_rect = pg.Rect(
            int(WIDTH * 0.1), int(HEIGHT * 0.1), int(WIDTH * 0.8), int(HEIGHT * 0.8)
        )

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
        self.screen.fill(self.biome.color[0], self.window_rect)
        if self.time_start:
            self._draw_timer()

    def _complete(self, successful: bool) -> None:
        """Called when task was completed."""
        logger.debug(successful)

        if successful:
            Sound.task_completed.play()
        else:
            Sound.task_failed.play()

        game_vars.open_task = None
        game_vars.current_heat += (
            self.heat_add_success if successful else self.heat_add_failure
        )

        game_vars.notification = Notification(
            self.biome.text_task_success if successful else self.biome.text_task_fail,
            Color.green if successful else Color.red,
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

    time_limit: float = 15

    maze: List["Cell"]

    maze_start: Tuple[int, int] = (5, 7)  # Y, X
    # width and height include the border of the maze
    maze_width: int = 15
    maze_height: int = 11

    # If the player has started the maze - moved mouse over start
    started: bool = False

    wall_image: pg.Surface
    path_image: pg.Surface
    start_image: pg.Surface
    end_image: pg.Surface

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cell_size = (
            self.window_rect.width // self.maze_width,
            self.window_rect.height // self.maze_height,
        )

        # Prepare images for the maze
        self.start_image = scale(
            load(str(self.biome.image_from(MAZE_START))).convert_alpha(), self.cell_size
        )

        self.end_image = scale(
            load(str(self.biome.image_from(MAZE_END))).convert_alpha(), self.cell_size
        )

        self.path_image = scale(
            load(str(self.biome.image_from(MAZE_PATH))).convert_alpha(), self.cell_size
        )

        self.wall_image = scale(
            load(str(self.biome.image_from(MAZE_WALL))).convert_alpha(), self.cell_size
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
                self.screen.blit(cell.image, cell.rect.topleft)

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
                image = self.path_image
                if cell == self.CellType.WALL:
                    image = self.wall_image
                elif cell == self.CellType.START:
                    image = self.start_image
                elif cell == self.CellType.END:
                    image = self.end_image
                self.maze.append(self.Cell(rect, image, cell))

                x += self.cell_size[0]
            y += self.cell_size[1]

    @dataclass
    class Cell:
        """Maze cell object class."""

        rect: pg.Rect
        image: pg.Surface
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
    heat_add_success: float = -2
    heat_add_failure: float = 0

    def start(self) -> None:
        """User clicks on task."""
        super().start()

        # set delay timer, mixing animation bool, and the choices of players
        self.delay = time()
        self.mixing = False
        self.choice = None
        self.computer_choice = None

        # other timers and states for the game
        self.game_over = False
        self.win = False
        self.timer = 0
        self.last = 0

        # get the colors from the current biombe
        self.color, self.color_hover = self.biome.color

        # calculate the size of the human choice rects and computer one
        # the human area of rects will be 1/9 of the whole task window
        # the computer area of rects will be 2/3 of the whole task window
        self.choice_rect_side = int(self.window_rect.height / 3)
        self.computer_rect_side = self.window_rect.height

        # store the three human choice rectangles in a list
        self.choice_rects = list()

        # create all human choice rectangles
        # they move from top to bottom on the y axis
        for i in range(3):
            self.choice_rects.append(
                pg.Rect(
                    self.window_rect.left,
                    self.choice_rect_side * i + self.window_rect.top,
                    self.choice_rect_side,
                    self.choice_rect_side,
                )
            )

        # create the large rectangle of the computer choice
        self.computer_rect = pg.Rect(
            self.window_rect.left + self.choice_rect_side,
            self.window_rect.top,
            self.computer_rect_side,
            self.computer_rect_side,
        )

        # the biome getters of the images of elements
        self.images = [ROCK, PAPER, SCISSORS]

        # store the images of the elements with different sizes
        # because the rectanglea are different
        self.choice_images = list()
        self.computer_images = list()

        # iterate the images
        for img in self.images:
            # load it from current biome and
            # scale it for human choice
            self.choice_images.append(
                scale(
                    load(str(self.biome.image_from(img))).convert_alpha(),
                    [self.choice_rect_side] * 2,
                )
            )
            # load it from current biome and
            # scale it for computer choice
            self.computer_images.append(
                scale(
                    load(str(self.biome.image_from(img))).convert_alpha(),
                    [self.computer_rect_side] * 2,
                )
            )
        # one more extra image for the computer
        # it is a question mark and displays it
        # till the human makes a choice
        self.computer_images.append(
            scale(
                load(str(self.biome.image_from(QUESTION_MARK))).convert_alpha(),
                [self.computer_rect_side] * 2,
            )
        )

    def update(self, event: pg.event) -> None:
        """Handles clicks, make computer choice and complete the task."""
        super().update()

        # iterate all human rect choices
        for i, rect in enumerate(self.choice_rects):
            mouse_hover = rect.collidepoint(pg.mouse.get_pos())
            mouse_click = event.type == pg.MOUSEBUTTONDOWN

            if (
                mouse_hover
                and mouse_click
                and self.choice not in [0, 1, 2]  # asserts that the human didn't chose
                and (time() - self.delay) > 0.3
            ):
                Sound.click.play()
                # if mouse clicked on button and not choosed yet
                self.choice = i
                self.mixing = True
                self.timer = time()
                # set timer for computer shuffling (animation)

        # make computer choose and evaluate if it is a win
        if not self.game_over and (time() - self.timer <= 0.5):
            self.computer_choice = randint(0, 2)

            # if it is draw
            if self.choice == self.computer_choice:
                self.win = False
            elif self.choice == 0:  # Rock
                if self.computer_choice == 1:  # vs Paper
                    self.win = False
                elif self.computer_choice == 2:  # vs Scissors
                    self.win = True
            elif self.choice == 1:  # Paper
                if self.computer_choice == 0:  # vs Rock
                    self.win = True
                elif self.computer_choice == 2:  # vs Scissors
                    self.win = False
            elif self.choice == 2:  # Scissors
                if self.computer_choice == 1:  # vs Paper
                    self.win = True
                elif self.computer_choice == 0:  # vs Rock
                    self.win = False
            self.game_over = True
            self.last = time()
            # set timer for lasting - not instant quit

        if self.game_over:
            if time() - self.last > 2:  # seconds of lasting
                if self.win:
                    return self._complete(True)
                else:
                    return self._complete(False)

    def draw(self) -> None:
        """Draws elements."""
        super().draw()
        # fill it biome color
        self.screen.fill(self.color, self.window_rect)

        if self.mixing and (time() - self.timer < 0.5):
            # draw the animation mixing for 0.5 seconds
            self.__draw_mixing()
        elif self.game_over and (time() - self.timer >= 0.5):
            # if it is not mixing anymore - draw the computer choice
            self.screen.blit(
                self.computer_images[self.computer_choice], self.computer_rect
            )
        else:
            # else blit the question mark
            self.screen.blit(self.computer_images[3], self.computer_rect)

        # draw choice images and hover states
        for rect in self.choice_rects:
            mouse_hover = rect.collidepoint(pg.mouse.get_pos())

            if mouse_hover:
                self.screen.fill(self.color_hover, rect)

        for i, rect in enumerate(self.choice_rects):
            self.screen.blit(self.choice_images[i], rect)

    def __draw_mixing(self):
        """Draws mixing animation of the computer choice."""
        rand_img = self.computer_images[randint(0, 2)]
        self.screen.blit(rand_img, self.computer_rect)


class TaskTicTacToe(Task):
    """
    Tic Tac Toe - players is playing a simple tic tac toe game against the computer.

    Task is themed around the biome this task spawned in.
    """

    # How much heat does success/failure add
    heat_add_success: float = -3
    heat_add_failure: float = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.game_over = False

        # human, computer and board representation
        self.human = -1
        self.computer = +1
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        # which is going to move first and the side of the board rect
        self.first_move = int()
        side = self.window_rect.height * 0.9

        # create Rect object (square for the board)
        self.board_rect = pg.Rect(
            int((self.window_rect.width - side) / 2 + self.window_rect.left),
            int(self.window_rect.height * 0.05 + self.window_rect.top),
            int(side),
            int(side),
        )

        # calculate the size of each cell and create a list to store them
        self.cell_side = int(self.board_rect.width / 3)
        self.cells = list()

        # create Rect object for each cell
        for y in range(3):
            for x in range(3):
                self.cells.append(
                    pg.Rect(
                        self.board_rect.left + (x * self.cell_side),
                        self.board_rect.top + (y * self.cell_side),
                        self.cell_side,
                        self.cell_side,
                    )
                )
        # save last click time - to prevent too much clicking of the button
        self.last_click = float()

        # get background and hover color from the biome context
        self.bg_color, self.bg_color_hover = self.biome.color

        # create map indexed
        # so we can use int to access the board cell

        # 0 - [0, 0], 1 - [0, 1], 2 - [0, 2]
        # 3 - [0, 0], 4 - [0, 1], 5 - [0, 2]
        # 6 - [0, 0], 7 - [0, 1], 8 - [0, 2]

        self.map_indexes = dict(
            zip(range(0, 9), [(i, j) for i in range(3) for j in range(3)])
        )

        # load the image of the X and O
        # X is always the human
        # O is always the computer

        self.x_image = scale(
            load(str(self.biome.image_from(X))).convert_alpha(), [self.cell_side] * 2
        )

        self.o_image = scale(
            load(str(self.biome.image_from(O))).convert_alpha(), [self.cell_side] * 2
        )

        # load the square grid image
        self.grid = scale(
            load(str(self.biome.image_from(TTT_GRID))).convert_alpha(),
            [self.board_rect.width, self.board_rect.height],
        )

    def start(self) -> None:
        """
        When user click on task - random decide the turn.

        Turn - human or computer.
        """
        super().start()

        # create delay timer to prevent clicking instantly
        # on cell after the click on the task
        self.delay = time()

        # get random choice - who is going to be first
        self.turn = choice([self.human, self.computer])

    def update(self, event: pg.event) -> None:
        """Handle events, user, input and makes computer moves."""
        super().update()

        # iterate all cells and check for events
        for i, cell in enumerate(self.cells):
            # click and hover - this means that the cell is clicked
            mouse_hover = cell.collidepoint(pg.mouse.get_pos())
            mouse_click = event.type == pg.MOUSEBUTTONDOWN

            x, y = self.map_indexes[i]  # take indexes from int
            empty_cell = self.board[x][y] == 0  # bool if the cell is empty

            if (
                mouse_click
                and mouse_hover
                and empty_cell
                and self.turn == self.human  # ensure that is a human turn
                and (time() - self.last_click) > 0.3  # prevent clicking too much
                and (time() - self.delay) > 0.3  # prevent clicking after task click
            ):
                # plays the clicking sound and saves last click
                Sound.click.play()
                self.last_click = time()

                # inserts human move into the board and gives turn to the computer
                self.__insert_human_move(i)
                # reverses the turn
                # 1 * -1 = -1
                # -1 * -1 = 1
                self.turn *= -1

        if not self.game_over and (
            self.__won(self.board, self.human) or len(self.__cells_left()) == 0
        ):
            # it is a win if the human player or there are no cells left to be filled

            # set one more timer to delay the switching to the game
            self.last = time()

            # states variables set
            self.game_over = True
            self.win = True

        if self.turn == self.computer:
            # if is computer turn - take the move and give turn to the human
            self.__make_computer_move()
            self.turn *= -1

        if not self.game_over and self.__won(self.board, self.computer):
            # if the computer won
            # set the same variables like in human win
            # the only difference is self.win
            self.last = time()
            self.game_over = True
            self.win = False

        if self.game_over:
            # if it game over - delay 0.5
            # prevents instantly switching to the game
            if time() - self.last > 0.5:
                # return the results
                # respectivly the task is completed if the human won
                if self.win:
                    return self._complete(True)
                else:
                    return self._complete(False)

    def draw(self) -> None:
        """Draw all elements and hover states."""
        super().draw()

        # fill the background of the board with color
        self.screen.fill(self.bg_color, self.board_rect)

        # iterate every cell
        for i, cell in enumerate(self.cells):
            x, y = self.map_indexes[i]
            # x, y are the indexes of the cell in matrix format

            if cell.collidepoint(pg.mouse.get_pos()) and self.board[x][y] == 0:
                # if the cell is hovered - fill it with different color
                self.screen.fill(self.bg_color_hover, cell)

            # draw the X and O images for the human and computer
            if self.board[x][y] == self.human:
                self.screen.blit(self.x_image, cell)
            elif self.board[x][y] == self.computer:
                self.screen.blit(self.o_image, cell)

        # draw the grid of
        self.screen.blit(self.grid, self.board_rect)

    def __won(self, board, player):
        """Checks  if given player is in winning positon."""
        # the winning positions in the Tic Tac Toe are 8
        # three horizontals
        # three verticals
        # two diagonals
        win_boards = [
            [board[0][0], board[0][1], board[0][2]],  # horizontal, 1 - row
            [board[1][0], board[1][1], board[1][2]],  # horizontal, 2 - row
            [board[2][0], board[2][1], board[2][2]],  # horizontal, 3 - row
            [board[0][0], board[1][0], board[2][0]],  # vertical, 1 - column
            [board[0][1], board[1][1], board[2][1]],  # vertical, 2 - column
            [board[0][2], board[1][2], board[2][2]],  # vertical, 3 - column
            [
                board[0][0],
                board[1][1],
                board[2][2],
            ],  # diagonal, top-left <> bottom-right
            [
                board[2][0],
                board[1][1],
                board[0][2],
            ],  # diagonal, top-right <> bottom-left
        ]

        # check if the player is anywere in the winning positions
        if 3 * [player] in win_boards:
            return True
        return False

    def __cells_left(self):
        """Returns a list of cordinates of empty cells."""
        # store the empty cells in a list
        cells = list()

        # enumerate all the rows and each cell in it
        for x, row in enumerate(self.board):
            for y, cell in enumerate(row):
                if cell == 0:
                    # the cell is empty - add its cordinates to the list
                    cells.append([x, y])
        return cells

    def __insert_human_move(self, cell):
        """Inserts human move in the board."""
        # take the x, y matrix indexes and insert the human symbol in the cell
        x, y = self.map_indexes[cell]
        self.board[x][y] = self.human

    def __make_computer_move(self):
        """The main algorithm for making a computer move."""
        # win in the next move
        for cell in self.__cells_left():
            x, y = cell
            self.board[x][y] = self.computer
            if self.__won(self.board, self.computer):
                self.board[x][y] = self.computer
                return
            else:
                self.board[x][y] = 0

        # block human win
        for cell in self.__cells_left():
            x, y = cell
            self.board[x][y] = self.human
            if self.__won(self.board, self.human):
                self.board[x][y] = self.computer
                return
            else:
                self.board[x][y] = 0

        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]

        # take corners
        shuffle(corners)
        for cor in corners:
            x, y = cor
            if self.board[x][y] == 0:
                self.board[x][y] = self.computer
                return

        # take center
        if self.board[1][1] == 0:
            self.board[1][1] = self.computer
            return

        # take random cell
        if len(self.__cells_left()) > 0:
            x, y = choice(self.__cells_left())
            self.board[x][y] = self.computer
