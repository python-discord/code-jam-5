import asyncio
import discord
import random
import string

from datetime import datetime
from discord.ext import commands


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
    def __init__(self, bot):
        self.bot = bot

        with open(WORDS_PATH, "r") as file:
            words = file.read().split("\n")

        self.word = words[random.randint(0, 10000)]
        self.guesses = []
        self.lives = 6

    def revealed(self):
        revealed_word = [char.upper() if char in self.guesses else "\_" for char in self.word]
        return " ".join(revealed_word)

    def is_finished(self):
        return all(char in self.guesses for char in self.word)

    @staticmethod
    def to_ascii(reaction: discord.Reaction):
        if reaction.emoji not in UNICODE_LETTERS:
            raise ValueError

        return string.ascii_lowercase[UNICODE_LETTERS.index(reaction.emoji)]

    @staticmethod
    async def clear_reactions(message: discord.Message):
        try:
            await message.clear_reactions()
        except (discord.Forbidden, discord.HTTPException):
            pass

    def hangman_embed(self, contents):
        fmt = f"{contents}\n\n```{HANGMAN_STATES[6 - self.lives]}```\n\nThe word is: {self.revealed()}\n\nLives: {self.lives}"
        embed = discord.Embed(colour=self.bot.colour,
                              title="Hangman Game",
                              description=fmt,
                              timestamp=datetime.utcnow())
        
        return embed

    @commands.command()
    async def hangman(self, ctx, *, member: discord.Member = None):
        embed = self.hangman_embed("Welcome to Hangman! Start the game by reacting to this message.")
        message: discord.Message = await ctx.send(
            embed=embed
        )

        while not self.is_finished() and self.lives > 0:
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

        if self.is_finished():
            await ctx.send(content=f"Congratulations! You solved the puzzle in {len(self.guesses)} guesses.")
        elif self.lives == 0:
            await ctx.send(content=f"Unfortunately, you died at {len(self.guesses)} guesses. The word was {self.word}.")


def setup(bot):
    bot.add_cog(Hangman(bot))
