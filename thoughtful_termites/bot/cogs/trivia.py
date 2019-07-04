import asyncio
import discord
import json
import random

from datetime import datetime
from discord.ext import commands

TRIVIA_QUESTIONS_PATH = './resources/trivia_questions.json'


class Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        with open(TRIVIA_QUESTIONS_PATH) as fp:
            self.raw_trivia_questions = json.load(fp)

        self.trivia_categories = set(n['category'] for n in self.raw_trivia_questions)
        self.trivia_difficulties = set(n['difficulty'] for n in self.raw_trivia_questions)

    def get_trivia_question(self, difficulty, category):
        random.shuffle(self.raw_trivia_questions)

        def pred(result):
            if category:
                if not result['category'] == category:
                    return False
            if difficulty:
                if not result['difficulty'] == difficulty:
                    return False
            return True

        question = discord.utils.find(pred, self.raw_trivia_questions)
        return question

    def prepare_embed(self, difficulty, category):
        letters = ['A', 'B', 'C', 'D']
        results = self.get_trivia_question(difficulty, category)

        answers = [n for n in results['incorrect_answers']]
        answers.append(results['correct_answer'])
        random.shuffle(answers)

        fmt = '\n'.join(f'{letters[i]}. {v}' for i, v in enumerate(answers))
        fmt = f"{fmt}\n\nDifficulty: {results['difficulty']}\nCategory: {results['category']}"

        embed = discord.Embed(colour=self.bot.colour,
                              title=results['question'],
                              description=fmt,
                              timestamp=datetime.utcnow())
        return embed, answers, results['correct_answer']

    async def do_trivia(self, ctx, difficulty, category):
        lookup = ['\N{REGIONAL INDICATOR SYMBOL LETTER A}',
                  '\N{REGIONAL INDICATOR SYMBOL LETTER B}',
                  '\N{REGIONAL INDICATOR SYMBOL LETTER C}',
                  '\N{REGIONAL INDICATOR SYMBOL LETTER D}'
                  ]
        embed, answers, correct_answer = self.prepare_embed(difficulty, category)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        msg = await ctx.send(embed=embed)
        for i in range(len(answers)):
            await msg.add_reaction(lookup[i])

        def check(r, u):
            if not (u == ctx.author and r.message.channel == ctx.channel):
                return False
            if not str(r) in lookup:
                return False
            return True

        reaction, user = await self.bot.wait_for('reaction_add', check=check)

        answer = answers[lookup.index(str(reaction))]
        correct = True if answer == correct_answer else False

        embed.description += f"\n\n{'Correct!' if correct else 'Incorrect.'} " \
                             f"The answer was:\n`{correct_answer}`"
        embed.colour = discord.Colour.green() if correct else discord.Colour.red()
        await msg.edit(embed=embed)
        try:
            await msg.clear_reactions()
        except (discord.Forbidden, discord.HTTPException):
            pass
        return correct

    @commands.group(invoke_without_command=True)
    async def trivia(self, ctx, difficulty: str = None, *, category: str = None):
        # TODO: Validate difficulty and category with custom converter
        if ctx.invoked_subcommand is not None:
            return
        await self.do_trivia(ctx, difficulty, category)

    @trivia.command()
    async def game(self, ctx, difficulty: str = None, *, category: str = None):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        msg = await ctx.send('How many rounds would you like to play? A number like `5`, or `20` would be appropriate.')
        try:
            rounds = await self.bot.wait_for('message', check=check, timeout=60.0)
        except asyncio.TimeoutError:
            return await ctx.send('You took too long. Goodbye...')
        try:
            rounds = int(rounds.clean_content)
        except ValueError:
            return await ctx.send('That wasn\'t a valid number. Goodbye...')
        if not rounds > 0:
            return await ctx.send('You can\'t have a negative number of rounds!')
        await msg.delete()

        attempts = 0
        wins = 0
        losses = 0
        for i in range(rounds):
            result = await self.do_trivia(ctx, difficulty, category)
            attempts += 1
            if result:
                wins += 1
            else:
                losses += 1

        fmt = f'Game Over!\nAttempts: {attempts}\nCorrect: {wins}\n' \
              f'Incorrect: {losses}\nCorrect: {int(wins/attempts*100)}%\n\n' \
              f'Thanks for playing!'
        await ctx.send(embed=discord.Embed(colour=self.bot.colour,
                                           description=fmt,
                                           timestamp=datetime.utcnow()
                                           )
                       )

    @trivia.command()
    async def categories(self, ctx):
        fmt = 'Categories:\n' + '\n'.join(f'•`{n}`' for n in self.trivia_categories)
        fmt += f"\n\nDifficulties:\n" + '\n'.join(f'•`{n}`' for n in self.trivia_difficulties)
        await ctx.send(embed=discord.Embed(colour=self.bot.colour,
                                           description=fmt,
                                           timestamp=datetime.utcnow()
                                           )
                       )



def setup(bot):
    bot.add_cog(Trivia(bot))
