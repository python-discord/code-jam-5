import enum
import random
from datetime import datetime

import discord
from discord.ext import commands

from thoughtful_termites.bot import unlocks


class Tile(enum.Enum):
    """
    An enum encapsulating every tile in Treefinder, either empty (i.e.
    not containing a mine) or that it contains a mine.
    """
    EMPTY = 0
    TREE = 1


class Treefinder(commands.Cog):
    """
    The cog that contains the mechanics of a Treefinder game.
    """
    def create_board(self):
        """
        Generates an empty Treefinder board, which is what `self.board`
        defaults to.

        :return: A 2D array (self.height * self.width) populated with Tile.EMPTY
        """
        board = []

        for x in range(self.height):
            row = []

            for y in range(self.width):
                row.append(Tile.EMPTY)

            board.append(row)

        return board

    def __init__(self, bot, width=9, height=9, trees=10):
        """
        Makes a new Treefinder class, used by setup().

        :param bot: ClimateBot
        :param width: the width of the Treefinder board, defaults to 9
        :param height: the height of the board, defaults to 9
        :param trees: the amount of trees in the board, defaults to 10
        """
        self.bot = bot

        self.width = width
        self.height = height
        self.trees = trees

        self.board = self.create_board()
        self.revealed = []
        self.flags = []

        self.mine_guessed = False

    def in_bounds(self, x, y):
        """
        Checks if a tile (x, y) is in-bounds, i.e. whether it's in the
        board or not. Note x is for the nth row, y is for the nth column.

        :param x: The xth row
        :param y: The yth column
        :return: Whether the tile is in-bounds or not
        """
        return 0 <= x < self.height and 0 <= y < self.width

    def surrounding_trees(self, x, y):
        """
        Given a tile (x, y), determines how many trees surround that tile.

        :param x: The xth row
        :param y: The yth column
        :return: How many trees surround (x, y)
        """
        coords = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
                  (x, y - 1), (x, y + 1),
                  (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]

        trees = 0

        for (a, b) in coords:
            if not self.in_bounds(a, b):
                continue

            if self.board[a][b] == Tile.TREE:
                trees += 1

        return trees

    def stringify_board(self):
        """
        Converts self.board into a string format suitable for displaying to a user.

        :return: A stringified version of self.board
        """
        string = []

        for x in range(self.height):
            row = ""

            for y in range(self.width):
                cell = self.board[x][y]

                if cell == Tile.EMPTY and (x, y) in self.revealed:
                    trees = self.surrounding_trees(x, y)
                    row += " " if trees == 0 else str(trees)
                elif (x, y) in self.flags:
                    row += "x"
                else:
                    row += "."

            string.append(row)

        return "\n".join(string)

    def reveal_at(self, x, y):
        """
        Reveal a tile at (x, y) (i.e. show how many trees surround this tile
        or, if (x, y) is a mine, end the game). If (x, y) has 0 trees surrounding
        it, reveal all tiles surrounding (x, y).

        :param x: The xth row of the tile revealed
        :param y: The yth column of the tile revealed
        """
        if not self.in_bounds(x, y):
            return

        if self.board[x][y] == Tile.TREE:
            self.mine_guessed = True
            return

        coords = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
                  (x, y - 1), (x, y + 1),
                  (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]

        self.revealed.append((x, y))

        if self.surrounding_trees(x, y) == 0:
            for (a, b) in coords:
                if (a, b) not in self.revealed:
                    self.reveal_at(a, b)

    def populate_trees(self, x, y):
        """
        Fill self.board with a given amount of trees, as long as (x, y)
        has 0 trees surrounding it (Microsoft Minesweeper).

        :param x: The xth row of the tile that was first clicked
        :param y: The yth column of the tile that was first clicked
        """
        coords = []

        for h in range(self.height):
            for w in range(self.width):
                if not (x - 1 <= h <= x + 1 or y - 1 <= w <= y + 1):
                    coords.append((h, w))

        mine_coords = random.sample(coords, self.trees)

        for (a, b) in mine_coords:
            self.board[a][b] = Tile.TREE

    def game_finished(self):
        """
        Check whether the game's finished, which can happen in two ways:

        1. the user uncovers a mine
        2. the user successfully avoids all trees, either by marking them with flags
        or not covering them at all

        :return: Whether the game's finished or not
        """
        tiles = self.width * self.height
        uncovered = tiles - len(self.revealed)

        return self.mine_guessed or uncovered == self.trees

    # Discord-specific functions

    def treefinder_embed(self):
        """
        Generates a discord.Embed for Treefinder.

        :return: A discord.Embed object to be sent via ctx.send()
        """
        fmt = f"```{self.stringify_board()}```"

        embed = discord.Embed(colour=self.bot.colour,
                              title="🌲 Treefinder 🌲",
                              description=fmt,
                              timestamp=datetime.utcnow())

        return embed

    @staticmethod
    def parse_command(string):
        """
        Given a Treefinder command (guess x y or flag x y), parse it
        and output the result

        :param string: The command entered by the user
        :return: A tuple containing all the information from the command
        """
        if string.startswith("guess "):
            x, y = string[6:].split()
            return "guess", int(x), int(y)
        elif string.startswith("flag "):
            x, y = string[5:].split()
            return "flag", int(x), int(y)

    @commands.command()
    async def treefinder(self, ctx, *, member: discord.Member = None):
        """
        The treefinder command called by the user. Call >treefinder to start.

        :param ctx: The context at which the command was called
        :param member: The member that called the command
        """
        if not unlocks.has_unlocked(ctx, "treefinder"):
            await ctx.send(unlocks.unlock_message("Treefinder"))
            return

        ctx.send(
            "Your task is to find all the trees in this area. "
            "Be careful not to accidentally cut down a tree!\n\n"
            "Type `guess x y` to excavate a tile, "
            "or type `flag x y` to flag whether a tile has a tree or not."
        )

        embed = self.treefinder_embed()
        message: discord.Message = await ctx.send(embed=embed)

        # The user must click on a 0 in their first click, so we set up a special
        # "first turn"
        response = await self.bot.wait_for(
            "message", check=lambda r: r.content.startswith("guess ")
        )

        _, x, y = self.parse_command(response.content)

        self.populate_trees(x, y)
        self.reveal_at(x, y)

        # Continue listening for responses and executing them while the game is
        # still going
        while not self.game_finished():
            embed = self.treefinder_embed()
            await message.edit(embed=embed)

            response = await self.bot.wait_for(
                "message",
                check=lambda r: r.content.startswith("guess ") or r.content.startswith("flag ")
            )
            command_type, x, y = self.parse_command(response.content)

            if command_type == "guess":
                self.reveal_at(x, y)
            elif command_type == "flag":
                self.flags.append((x, y))

        # Check whether the user finished by winning or losing
        if self.mine_guessed:
            await ctx.send("Unfortunately, you lost the game!")
        else:
            await ctx.send("Congratulations, you found all the trees!")


def setup(bot):
    bot.add_cog(Treefinder(bot))
