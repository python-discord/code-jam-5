import asyncio
import random
import string

import discord
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
    def __init__(self, bot: discord.ext.commands.Bot):
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

    def hangman_message(self, contents):
        return f"{contents}\n\n```{HANGMAN_STATES[6 - self.lives]}```\n\nThe word is: {self.revealed()}\n\nLives: {self.lives} "

    @commands.command()
    async def hangman(self, ctx, *, member: discord.Member = None):
        message: discord.Message = await ctx.send(
            self.hangman_message("Welcome to Hangman! Start the game by reacting to this message.")
        )

        while not self.is_finished() and self.lives > 0:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60)
            except asyncio.TimeoutError:
                return await ctx.send("You took too long. Goodbye...")

            try:
                letter = self.to_ascii(reaction)
            except ValueError:
                return await ctx.send("Incorrect reaction. Goodbye...")

            if letter in self.guesses:
                await message.edit(
                    content=self.hangman_message("You've already guessed this letter!")
                )
                await self.clear_reactions(message)

                continue

            self.guesses += letter

            if letter in self.word:
                await message.edit(
                    content=self.hangman_message("You guessed a new letter! Congratulations!")
                )
            else:
                self.lives -= 1
                await message.edit(
                    content=self.hangman_message("You guessed a wrong letter!")
                )

            await self.clear_reactions(message)

        if self.is_finished():
            await message.edit(content=f"Congratulations! You solved the puzzle in {len(self.guesses)} guesses.")
            await self.clear_reactions(message)
        elif self.lives == 0:
            await message.edit(content=f"Unfortunately, you died at {len(self.guesses)} guesses. The word was {self.word}.")
            await self.clear_reactions(message)


def setup(bot):
    bot.add_cog(Hangman(bot))
