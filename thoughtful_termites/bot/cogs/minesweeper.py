import enum
import random
from datetime import datetime

import discord
from discord.ext import commands


class Tile(enum.Enum):
    EMPTY = 0
    MINE = 1


class Minesweeper(commands.Cog):
    def create_board(self):
        board = []

        for x in range(self.height):
            row = []

            for y in range(self.width):
                row.append(Tile.EMPTY)

            board.append(row)

        return board

    def __init__(self, bot, width=9, height=9, mines=10):
        self.bot = bot

        self.width = width
        self.height = height
        self.mines = mines

        self.board = self.create_board()
        self.revealed = []
        self.flags = []

        self.mine_guessed = False

    def in_bounds(self, x, y):
        return 0 <= x < self.height and 0 <= y < self.width

    def surrounding_mines(self, x, y):
        coords = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
                  (x, y - 1), (x, y + 1),
                  (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]

        mines = 0

        for (a, b) in coords:
            if not self.in_bounds(a, b):
                continue

            if self.board[a][b] == Tile.MINE:
                mines += 1

        return mines

    def stringify_board(self):
        string = []

        for x in range(self.height):
            row = ""

            for y in range(self.width):
                cell = self.board[x][y]

                if cell == Tile.EMPTY and (x, y) in self.revealed:
                    mines = self.surrounding_mines(x, y)
                    row += " " if mines == 0 else str(mines)
                elif (x, y) in self.flags:
                    row += "x"
                else:
                    row += "."

            string.append(row)

        return "\n".join(string)

    def reveal_at(self, x, y):
        if not self.in_bounds(x, y):
            return

        if self.board[x][y] == Tile.MINE:
            self.mine_guessed = True
            return

        coords = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
                  (x, y - 1), (x, y + 1),
                  (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]

        self.revealed.append((x, y))

        if self.surrounding_mines(x, y) == 0:
            for (a, b) in coords:
                if (a, b) not in self.revealed:
                    self.reveal_at(a, b)

    def fill_mines(self, x, y):
        coords = []

        for h in range(self.height):
            for w in range(self.width):
                if not (x - 1 <= h <= x + 1 or y - 1 <= w <= y + 1):
                    coords.append((h, w))

        mine_coords = random.sample(coords, self.mines)

        for (a, b) in mine_coords:
            self.board[a][b] = Tile.MINE

    def game_finished(self):
        tiles = self.width * self.height
        uncovered = tiles - len(self.revealed)

        return self.mine_guessed or uncovered == self.mines

    # Discord-specific functions

    def minesweeper_embed(self, message):
        fmt = f"{message}\n\n```{self.stringify_board()}```"

        embed = discord.Embed(colour=self.bot.colour,
                              title="Minesweeper",
                              description=fmt,
                              timestamp=datetime.utcnow())

        return embed

    def parse_command(self, string):
        if string.startswith("guess "):
            x, y = string[6:].split()
            return "guess", int(x), int(y)
        elif string.startswith("flag "):
            x, y = string[5:].split()
            return "flag", int(x), int(y)

    @commands.command()
    async def minesweeper(self, ctx, *, member: discord.Member = None):
        embed = self.minesweeper_embed("Type `guess x y` to guess a tile.")
        message: discord.Message = await ctx.send(embed=embed)

        response = await self.bot.wait_for("message", check=lambda r: r.content.startswith("guess "))
        _, x, y = self.parse_command(response.content)

        self.fill_mines(x, y)
        self.reveal_at(x, y)

        while not self.game_finished():
            embed = self.minesweeper_embed("You can also flag mines by doing `flag x y`.")
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

        if self.mine_guessed:
            await ctx.send("Unfortunately, you lost the game!")
        else:
            await ctx.send("Congratulations, you uncovered all the mines!")


def setup(bot):
    bot.add_cog(Minesweeper(bot))
