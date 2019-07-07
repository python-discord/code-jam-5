import asyncio
import discord
import random
import string

from datetime import datetime
from discord.ext import commands

from thoughtful_termites.bot import unlocks

WORDS_PATH = "./resources/hangman_words.txt"

HANGMAN_STATES = ['''
  +---+
  |   |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\\  |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\\  |
 /    |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\\  |
 / \\  |
      |
=========''']

UNICODE_LETTERS = [
    "🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱", "🇲",
    "🇳", "🇴", "🇵", "🇶", "🇷", "🇸", "🇹", "🇺", "🇻", "🇼", "🇽", "🇾", "🇿"
]


class Hangman(commands.Cog):
    """
    The cog that contains the mechanics for the Hangman game.
    """
    def __init__(self, bot):
        """
        Initialise the state for a Hangman game, and chooses a random word
        from Google's 10,000 most common words as the word to be guessed.

        :param bot: ClimateBot, used for setup()
        """
        self.bot = bot

        with open(WORDS_PATH, "r") as file:
            words = file.read().split("\n")

        self.word = words[random.randint(0, 10000)]
        self.guesses = []
        self.lives = 6

    def revealed(self):
        """
        Displays the word as capital letters and underscores (e.g. "_ _ _ _" for a
        4-letter word).

        :return: A human-readable version of the partially-guessed word
        """
        revealed_word = [char.upper() if char in self.guesses else "\\_" for char in self.word]
        return " ".join(revealed_word)

    def is_finished(self):
        """
        Checks if the game is finished, which is by guessing all the letters or dying.

        :return: Whether the game is finished
        """
        return self.lives == 0 or all(char in self.guesses for char in self.word)

    @staticmethod
    def to_ascii(reaction: discord.Reaction):
        """
        Converts a Discord reaction emoji into an ASCII character.

        :param reaction: The reaction which the user sent
        :return: The ASCII character corresponding to that reaction
        """
        if reaction.emoji not in UNICODE_LETTERS:
            raise ValueError

        return string.ascii_lowercase[UNICODE_LETTERS.index(reaction.emoji)]

    @staticmethod
    async def clear_reactions(message: discord.Message):
        """
        Clear all reactions from a message.

        :param message: The message that needs to have its reactions cleared
        """
        try:
            await message.clear_reactions()
        except (discord.Forbidden, discord.HTTPException):
            pass

    def hangman_embed(self, contents):
        """
        Generates a discord.Embed for Hangman, given an initial message.

        :param contents: The contents of the Hangman embed, placed at the top
        :return: A discord.Embed with all the Hangman information on it
        """
        fmt = f"{contents}\n\n```{HANGMAN_STATES[6 - self.lives]}```\n\nThe word is: {self.revealed()}\n\nLives: {self.lives}"
        embed = discord.Embed(colour=self.bot.colour,
                              title="Hangman Game",
                              description=fmt,
                              timestamp=datetime.utcnow())
        
        return embed

    @commands.command()
    async def hangman(self, ctx, *, member: discord.Member = None):
        """
        The Hangman command called by the user. Call >hangman to start.

        :param ctx: The context at which the command was called
        :param member: The member that called the command
        """
        if not unlocks.has_unlocked(ctx, "hangman"):
            await ctx.send(unlocks.unlock_message("Hangman"))
            return

        embed = self.hangman_embed("Welcome to Hangman! Start the game by reacting to this message.")
        message: discord.Message = await ctx.send(
            embed=embed
        )

        while not self.is_finished():
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60)
            except asyncio.TimeoutError:
                await ctx.send("You took too long. Goodbye...")
                return

            try:
                letter = self.to_ascii(reaction)
            except ValueError:
                await ctx.send("Incorrect reaction. Goodbye...")
                return

            if letter in self.guesses:
                await message.edit(
                    embed=self.hangman_embed("You've already guessed this letter!")
                )

                try:
                    await message.clear_reactions()
                except (discord.Forbidden, discord.HTTPException):
                    pass

                continue

            self.guesses += letter

            if letter in self.word:
                embed.colour = discord.Colour.green()
                await message.edit(
                    embed=self.hangman_embed("You guessed a new letter! Congratulations!")
                )
            else:
                self.lives -= 1
                embed.colour = discord.Colour.red()
                await message.edit(
                    embed=self.hangman_embed("You guessed a wrong letter!")
                )

            try:
                await message.clear_reactions()
            except (discord.Forbidden, discord.HTTPException):
                pass

        await message.delete()

        if self.lives == 0:
            await ctx.send(content=f"Unfortunately, you died at {len(self.guesses)} guesses. The word was {self.word}.")
        else:
            await ctx.send(content=f"Congratulations! You solved the puzzle in {len(self.guesses)} guesses.")


def setup(bot):
    bot.add_cog(Hangman(bot))
