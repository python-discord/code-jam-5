import asyncio
import discord
import json
import random
import typing

from datetime import datetime
from discord.ext import commands

from thoughtful_termites.bot.resources import trivia_questions_path, climate_arguments_path
from thoughtful_termites.bot.unlocks import has_unlocked


class CategoryConverter(commands.Converter):
    async def convert(self, ctx, argument):
        """Ensures arguments are valid categories for `>trivia` commands.
        """
        cog = ctx.bot.get_cog('Trivia')
        if not cog:
            raise RuntimeError('Trivia cog not loaded.')

        argument = argument.lower()
        valid_categories = cog.trivia_categories

        if argument not in valid_categories:
            raise commands.BadArgument(
                f"Valid category not supplied. "
                f"Try one of the following:\n" + '\n'.join(
                    f'•`{n}`' for n in valid_categories
                )
            )

        return argument


class DifficultyConverter(commands.Converter):
    async def convert(self, ctx, argument):
        """Ensures arguments are valid difficulties for `>trivia` commands.
        """
        cog = ctx.bot.get_cog('Trivia')
        if not cog:
            raise RuntimeError('Trivia cog not loaded.')

        argument = argument.lower()
        valid_difficulties = cog.trivia_difficulties

        if argument not in valid_difficulties:
            raise commands.BadArgument(
                f"Valid difficulty not supplied. "
                f"Try one of the following:\n" + '\n'.join(
                    f'•`{n}`' for n in valid_difficulties
                )
            )

        return argument


class Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        with open(trivia_questions_path) as fp:
            self.raw_trivia_questions = json.load(fp)

        with open(climate_arguments_path) as fp:
            self.raw_climate_arguments = json.load(fp)

        self.trivia_categories = set(n['category'].lower() for n in self.raw_trivia_questions)
        self.trivia_difficulties = set(n['difficulty'].lower() for n in self.raw_trivia_questions)

    async def cog_command_error(self, ctx, error):
        if isinstance(error, (commands.BadArgument, commands.CheckFailure)):
            return await ctx.send(str(error))
        if isinstance(error, commands.BadUnionArgument):
            await ctx.send('Error encountered with parameters passed! '
                           'Please see examples for help...')
            return await ctx.send_help(ctx.command)

    def get_trivia_question(self, difficulty, category):
        """Returns a random trivia entry with given difficulty and category.
        """
        random.shuffle(self.raw_trivia_questions)

        def pred(result):
            if category:
                if not result['category'].lower() == category:
                    return False
            if difficulty:
                if not result['difficulty'].lower() == difficulty:
                    return False
            return True

        question = discord.utils.find(pred, self.raw_trivia_questions)
        return question

    def prepare_embed(self, difficulty, category):
        """Returns a formatted discord embed, possible and correct
        answers for a trivia difficult and category.
        """
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
        """Run a single trivia question.
        This function sends and adds reactions to a formatted embed,
        and waits for a response from the user.
        It will then edit the message as appropriate if the answer is correct/incorrect,
        notifying the user the result.
        """
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
    async def trivia(self, ctx, difficulty: typing.Union[DifficultyConverter,
                                                         CategoryConverter] = None,
                     *, category: CategoryConverter = None):
        """Complete a single trivia round.

        Parameters
        -----------------
        • Difficulty: a valid difficulty found with `>trivia difficulties`.
            This defaults to all difficulties.
        • Category: a valid category found with `>trivia categories`.
            This defaults to include all categories.

        Examples
        -----------------
        • `>trivia`
        • `>trivia easy`
        • `>trivia hard Animals`
        • `>trivia "Entertainment: Japanese Anime & Manga"
        • `>trivia Geography`
        """
        if ctx.invoked_subcommand is not None:
            return

        if difficulty not in self.trivia_difficulties:
            category = difficulty
            difficulty = None

        await self.do_trivia(ctx, difficulty, category)

    @trivia.command()
    async def game(
            self, ctx,

            difficulty: typing.Union[
                DifficultyConverter,
                CategoryConverter
            ] = None,

            *,

            category: CategoryConverter = None
    ):
        """Complete a trivia game with multiple rounds.
        The bot will prompt you with how many rounds you wish to play.
        An appropriate answer would be `5`, or `20` etc.

        Parameters
        -----------------
        • Difficulty: a valid difficulty found with `>trivia difficulties`.
            This defaults to all difficulties.
        • Category: a valid category found with `>trivia categories`.
            This defaults to include all categories.

        Examples
        -----------------
        • `>trivia`
        • `>trivia easy`
        • `>trivia hard Animals`
        • `>trivia "Entertainment: Japanese Anime & Manga"
        • `>trivia Geography`
        """
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        msg = await ctx.send('How many rounds would you like to play? '
                             'A number like `5`, or `20` would be appropriate.')
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

        fmt = f'Attempts: {attempts}\nCorrect: {wins}\n' \
              f'Incorrect: {losses}\nCorrect: {int(wins/attempts*100)}%\n\n' \
              f'Thanks for playing!'
        await ctx.send(embed=discord.Embed(colour=self.bot.colour,
                                           title='Game Over!',
                                           description=fmt,
                                           timestamp=datetime.utcnow()
                                           )
                       )

    @trivia.command()
    async def categories(self, ctx):
        """Returns a list of all trivia categories and difficulties.

        Example
        -------------
        • `>trivia categories`
        • `>trivia difficulties`

        Aliases
        --------------
        • `>trivia categories` (primary)
        • `>trivia difficulties`
        """
        fmt = 'Categories:\n' + '\n'.join(f'•`{n}`' for n in self.trivia_categories)
        fmt += f"\n\nDifficulties:\n" + '\n'.join(f'•`{n}`' for n in self.trivia_difficulties)
        await ctx.send(embed=discord.Embed(colour=self.bot.colour,
                                           description=fmt,
                                           timestamp=datetime.utcnow()
                                           )
                       )

    @commands.command(aliases=['cc', 'climcom'])
    @has_unlocked('commentary')
    async def climate_commentary(self, ctx, argument_id: int = None):
        """Get a random climate commentary.

        Parameters
        --------------
        Pass in any of the following:
            • Argument ID - The Argument ID to fetch. If None is passed, it will find a random one.

        Example
        ------------
        `?climate_commentary`
        `?cc 192`

        Aliases
        -----------
        `?climate_commentary` (primary)
        `?cc`
        `?climcom`
        """
        if not argument_id:
            argument_id = random.randint(0, len(self.raw_climate_arguments) - 1)

        if not 0 < argument_id < len(self.raw_climate_arguments):
            raise commands.BadArgument(
                f'Argument ID must be between 0 and {len(self.raw_climate_arguments)}'
            )

        choice = self.raw_climate_arguments[argument_id]
        embed = discord.Embed(colour=self.bot.colour,
                              title='Random Climate Commentary',
                              description=choice['body'],
                              timestamp=datetime.utcnow())
        embed.set_footer(text=f'This was ID No. {argument_id}')
        await ctx.send(embed=embed)


def setup(bot):
    with open(trivia_questions_path) as fp:
        print(set(n["difficulty"].lower() for n in json.load(fp)))

    bot.add_cog(Trivia(bot))
