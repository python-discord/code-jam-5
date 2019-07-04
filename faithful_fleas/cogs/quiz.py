import asyncio
import json
import logging
import random
from pathlib import Path

import discord
from discord.ext import commands


logger = logging.getLogger(__name__)


class ClimateQuiz(commands.Cog):
    """A cog for a simple quiz on Climate Changes."""
    def __init__(self, bot):
        self.bot = bot
        self.quizdata = self.load_json()
        self.question_limit = 3
        self.points = 0
        self.done_questions = []

    @staticmethod
    def load_json():
        p = Path('faithful_fleas', 'Resources', 'quiz.json')
        with p.open() as f:
            json_data = json.load(f)
            # print(json_data)
            return json_data['quiz_data']

    @commands.group(name='quiz', invoke_without_command=True)
    async def quiz_facts(self, ctx):
        await ctx.invoke(self.bot.get_command("help"), "quiz")

    @quiz_facts.command(name='start', aliases=['s'])
    async def start_quiz(self, ctx):
        await ctx.send(f"Quiz is going to start now! Get ready {ctx.author.mention}")
        await asyncio.sleep(2)
        await self.send_question(ctx)

    async def send_question(self, ctx):
        new_question = False
        question_data = random.choice(self.quizdata)
        while new_question is False:
            if question_data['id'] in self.done_questions:
                question_data = random.choice(self.quizdata)
            else:
                new_question = True
        self.done_questions.append(question_data['id'])
        question_number = len(self.done_questions)
        if question_number == self.question_limit:
            await ctx.send("This is the last question in the round!")
            await asyncio.sleep(2)
        question = question_data['question']
        embed = discord.Embed(colour=discord.Colour.green())
        embed.title = f"#{question_number}\n{question}"
        for i, option in enumerate(question_data['options']):
            embed.add_field(name=f"{i+1}) {option}", value='\u200b', inline=True)
        embed.set_footer(text=f"You answer should be in the form of option number.Example: \".quiz a 1\"")
        await ctx.send(embed=embed)

    @quiz_facts.command(name='answer', aliases=['a'])
    async def answer(self, ctx, answer: int):
        question_data = []
        question_id = self.done_questions[-1]
        for data in self.quizdata:
            if data["id"] == question_id:
                question_data = data

        if answer in question_data["answer"]:
            self.points += 1
            if question_data["fact"] == "":
                title = "Yay! You got it right!"
                des = ""
            else:
                title = "Yay! You got it right! Here is the fact related to that question."
                des = question_data["fact"]
            embed = discord.Embed(colour=discord.Colour.green())
            embed.title = title
            embed.description = des + '\n'
            embed.description += f"Your score is :tada:{self.points}/{len(self.done_questions)}"

        else:
            embed = discord.Embed(colour=discord.Colour.green())
            score_msg = f"You score is {self.points}/{len(self.done_questions)}"
            embed.title = 'Oops! You got it wrong buddy.'
            embed.add_field(name=f"The correct answer is:", value=f"{question_data['answer'][0]}\n\n{score_msg}", inline=True)
            if question_data["fact"] != "":
                embed.add_field(name="Here is the fact:", value=question_data["fact"], inline=True)
            else:
                pass
        await ctx.send(embed=embed)
        await asyncio.sleep(2)
        question_number = len(self.done_questions)
        if question_number == self.question_limit:
            await ctx.send("The quiz game ends here! Hope you had fun playing this.")
        else:
            embed.set_footer(text="Do \".quiz quit\" to exit the quiz.")

            await ctx.send("Lets move on to the next round!")
            await asyncio.sleep(2)
            await self.send_question(ctx)


def setup(bot):
    logger.info("ClimateQuiz cog loaded.")
    bot.add_cog(ClimateQuiz(bot))
