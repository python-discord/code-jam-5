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

    def get_trivia_question(self, difficulty, category):
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

    @commands.group()
    async def trivia(self, ctx, difficulty: str=None, *, category: str=None):
        lookup = {'\N{REGIONAL INDICATOR SYMBOL LETTER A}': 0,
                  '\N{REGIONAL INDICATOR SYMBOL LETTER B}': 1,
                  '\N{REGIONAL INDICATOR SYMBOL LETTER C}': 2,
                  '\N{REGIONAL INDICATOR SYMBOL LETTER D}': 3
                  }
        embed, answers, correct_answer = self.prepare_embed(difficulty, category)
        embed.set_author(name=ctx.author, icon_url=ctx.author.icon_url)
        msg = await ctx.send(embed=embed)
        for i in range(len(answers)):
            await msg.add_reaction(lookup.keys()[i])

        def check(r, u):
            if not u.id == ctx.author.id:
                return False
            if not r.channel.id == ctx.channel.id:
                return False
            if not str(r) in lookup:
                return False
            return True

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            embed.description += f"\n\nTimed out waiting. The correct answer was:\n`{correct_answer}`"
            await msg.edit(embed=embed)
            try:
                await msg.clear_reactions()
            except (discord.Forbidden, discord.HTTPException):
                pass
            return

        answer = answers[lookup[str(reaction)]]
        if answer == correct_answer:
            correct = True
        else:
            correct = False
        embed.description += f"\n\n{'Correct!' if correct else 'Incorrect.'} " \
                             f"The answer was:\n`{correct_answer}`"
        embed.colour = discord.Colour.green() if correct else discord.Colour.red()
        await msg.edit(embed=embed)
        try:
            await msg.clear_reactions()
        except (discord.Forbidden, discord.HTTPException):
            pass
        return

    @trivia.command()
    async def game(self, ctx, difficulty: str=None, *, category: str=None):
        # 1. Prompt: do you want friends?
        # 2. Wait for friends if so
        # 3. Start game
        # 4. 5 questions each
        # 5. Winner found
        pass


def setup(bot):
    bot.add_cog(Trivia(bot))
