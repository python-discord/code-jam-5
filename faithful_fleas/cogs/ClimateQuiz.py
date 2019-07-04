import asyncio
import json
import logging
import random
from pathlib import Path

import discord
from discord.ext import commands


logger = logging.getLogger(__name__)


emojis = {
    "1": "\U00000031\U000020E3",
    "2": "\U00000032\U000020E3",
    "3": "\U00000033\U000020E3",
    "4": "\U00000034\U000020E3",
    "5": "\U00000035\U000020E3"
}


class ClimateQuiz(commands.Cog):
    """A cog for a simple quiz on Climate Changes."""

    def __init__(self, bot):
        """Init function"""

        self.bot = bot
        self.quizdata = self.load_json()
        self.question_limit = 5  # Number of questions per start.
        self.reset_times = 0
        self.points = 0
        self.done_questions = []  # Questions which are already asked.
        self.question_number = 0
        self.player = 0
        self.message_to_react = ''

    @staticmethod
    def load_json():
        """A function to get the json data from a resource file."""

        p = Path('faithful_fleas', 'Resources', 'quiz.json')
        with p.open(encoding="utf8") as f:
            json_data = json.load(f)
            # print(json_data)
            return json_data['quiz_data']

    @commands.group(name='quiz', invoke_without_command=True)
    async def climate_quiz(self, ctx):
        """A set of commands to play the ClimateQuiz! use the start command to begin playing."""

        await ctx.send_help('quiz')

    @climate_quiz.command(name='start', aliases=['s'])
    async def start_quiz(self, ctx):
        """Starts the quiz."""

        # Checking if the user already started the quiz.
        if self.player != 0:
            return await ctx.send("You are already in a game!You have to quit that game first.")
        self.player = ctx.author.id

        # Intro
        await ctx.send(f"Quiz is going to start now! Get ready {ctx.author.mention}"
                       f"You might get two crazy question on the first "
                       f"quiz try if your lucky enough xD")
        await asyncio.sleep(1)
        await self.send_question(ctx.channel)

    async def send_question(self, channel):
        """This function gets a random question and sends it to the user."""

        new_question = False
        question_data = random.choice(self.quizdata)

        # making sure that the same questions are not asked.

        while new_question is False:
            if question_data['id'] in self.done_questions:
                question_data = random.choice(self.quizdata)
            else:
                new_question = True

        # Keeping track of asked questions.
        self.done_questions.append(question_data['id'])
        self.question_number += 1

        # To check if its the final round or not
        if self.question_number == self.question_limit:
            await channel.send("This is the final round!")
            self.reset_times += 1
            await asyncio.sleep(2)

        question = question_data['question']
        embed = discord.Embed(colour=discord.Colour.green())
        embed.title = f"#{self.question_number}\n{question}"
        embed.description = f"Question Type: {question_data['type']}"

        # sending the options in from of new fields.
        for i, option in enumerate(question_data['options']):
            embed.add_field(
                name=f"{i+1}) {option}",
                value='\u200b',
                inline=True
            )

        embed.set_footer(text=f"React to the corresponding number to give your answer.")

        # noting the message to which reactions are to be added.
        self.message_to_react = await channel.send(embed=embed)

        # Adding reactions to the embed so that the user can choose an answer.
        for i in range(0, len(question_data["options"])):
            values = list(emojis.values())
            await self.message_to_react.add_reaction(values[i])

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """
        Its a event that checks whether someone had reacted to a message.

        I am using this function to retrieve the option chosen by the user.
        """
        user = int(payload.user_id)
        message = payload.message_id

        # Only considering those reactions made the user who started the quiz.
        if user == self.player:

            # Making sure if its the same message(the embed)
            if int(message) == int(self.message_to_react.id):
                value_list = list(emojis.values())

                for i in value_list:
                    # Geting the reaction which the user reacted.
                    if str(payload.emoji) == i:
                        emoji_number = value_list.index(i) + 1
                        channel = self.message_to_react.channel
                        await self.reponse(emoji_number, channel)
                        break

    async def reponse(self, answer: int, channel):
        """This function is being used to send the reponse to the user's selected option."""

        question_data = []
        question_id = self.done_questions[-1]

        # First to get the question for which the user is answering to.
        for data in self.quizdata:
            if data["id"] == question_id:
                question_data = data

        # If the answer matches.
        if answer == question_data["answer"]:
            self.points += 1
            embed = discord.Embed(colour=discord.Colour.green())
            embed.title = "Yay! You got it right! Here is the fact related to that question."
            embed.description = question_data["fact"] + "\n \n"
            embed.description += f"Your score is :tada: {self.points} " \
                                 f"out of {len(self.done_questions)}"

        # If the answer does not match.
        else:
            embed = discord.Embed(colour=discord.Colour.green())
            score_msg = f"You score is {self.points} out of {len(self.done_questions)}"
            embed.title = 'Oops! You got it wrong buddy.'

            embed.add_field(
                name=f"The correct answer is:",
                value=f"{question_data['answer']}\n\n{score_msg}",
                inline=True)

            embed.add_field(
                name="Here is the fact:",
                value=question_data["fact"],
                inline=True)

        await channel.send(embed=embed)
        await asyncio.sleep(2)

        # checking if its end of quiz.
        if self.question_number == self.question_limit:
            self.reset_game()
            await channel.send("The quiz game ends here! Hope you had fun playing this.\n"
                               " Do `.quiz start` to play again if you were unlucky"
                               " and missed those crazy questions :grin:")
        else:
            embed.set_footer(text="Do \".quiz quit\" to exit the quiz.")

            await channel.send("Lets move on to the next round!")
            await asyncio.sleep(2)
            await self.send_question(channel)

    @climate_quiz.command(name='quit')
    async def quit_game(self, ctx):
        """Quit the quiz."""

        # Checking if the user has he started the quiz or not.
        if self.player == "":
            return await ctx.send("You are not in any game!")
        await ctx.send(f"You quit the game and your score is {self.points}"
                       f" out of {len(self.done_questions)}")
        self.reset_times += 1
        self.reset_game()

    def reset_game(self):
        """
        Reset the points and question number to 0 for smooth working when user wants to play again.

        Note I am not reseting the done_questions because when the user plays again,
        he will not get the same questions.
        """
        self.question_number = 0
        self.player = 0
        if self.reset_times == 3:
            self.points = 0
            self.reset_times = 0
            self.done_questions = []


def setup(bot):
    """Function to load the cog."""

    logger.info("ClimateQuiz cog loaded.")
    bot.add_cog(ClimateQuiz(bot))
