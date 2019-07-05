import enum

import discord
from discord.ext import commands


class Tile(enum.Enum):
    EMPTY = 0
    MINE = 1


class Minesweeper(commands.Cog):
    @staticmethod
    def create_board(width, height):
        board = []

        for _ in range(width):
            row = []

            for _ in range(height):
                row.append(Tile.EMPTY)

            board.append(row)

        return board

    def __init__(self, width=9, height=9):
        self.board = self.create_board(width, height)
        self.first_guess = True

    def stringify_board(self):
        pass

    @commands.command()
    def minesweeper(self, ctx, *, member: discord.Member = None):
        pass
