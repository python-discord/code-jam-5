import csv
import random
from datetime import datetime

import discord
from discord.ext import commands

from thoughtful_termites.bot import unlocks
from thoughtful_termites.bot.resources import rankings_data_path


class Rankings(commands.Cog):
    """
    The cog that contains the mechanics for the Rankings game.
    """
    def __init__(self, bot):
        """
        Initialise the states for the ranking game, taking raw statistics
        from rankings_data.csv.

        :param bot: ClimateBot, used by setup()
        """
        self.bot = bot

        with open(rankings_data_path, "r", encoding="utf-8-sig") as f:
            self.raw_rankings = list(csv.DictReader(f))

    @staticmethod
    def to_ranks(ls: list):
        """
        Given a list of values, return their "ranks" from smallest to largest.

        :param ls: A possibly unsorted list of numerical values
        :return: A list of those values' ranks (e.g. [1, 3, 4, 5, 2])
        """
        sorted_ls = sorted(ls)
        ranks = []

        for item in sorted_ls:
            ranks.append(5 - ls.index(item))

        return ranks

    @staticmethod
    def ranks_to_string(ls):
        """
        Convert raw statistics data, as well as the user's predicted ranks,
        into a human-readable format.

        :param ls: The list containing country statistics and user-predicted ranks
        :return: A human-readable version of that list
        """
        rows = []
        choices = "ABCDE"

        for n in range(len(ls)):
            country = ls[n]
            choice = choices[n]

            description = f"{choice}. {country['nation']}"

            if country["rank"] is not None:
                description += f" (Predicted rank {country['rank']})"

            rows.append(description)

        return "\n".join(rows)

    def rankings_embed(self, message, rankings):
        """
        Generates a discord.Embed for the Rankings game.

        :param message: The message to display at the top of the discord.Embed
        :param rankings: The country/user-prediction data
        :return: A discord.Embed carrying all of that information
        """
        fmt = f"{message}\n\n{self.ranks_to_string(rankings)}"

        embed = discord.Embed(colour=self.bot.colour,
                              title="Ranking Game",
                              description=fmt,
                              timestamp=datetime.utcnow())

        return embed

    @commands.command()
    async def rankings(self, ctx, *, member: discord.Member = None):
        """
        The Rankings command called by the user. Call >rankings to start.

        :param ctx: The context at which the command was called
        :param member: The member that called the command
        """
        if not unlocks.has_unlocked(ctx, "rankings"):
            await ctx.send(unlocks.unlock_message("Rankings"))
            return

        question_type = random.random()
        countries = random.sample(self.raw_rankings, 5)

        if question_type < 0.5:
            # Rank by carbon emissions overall
            ranks = self.to_ranks([x["total"] for x in countries])
            question = "Sort these countries by their total carbon dioxide emissions."
        else:
            # Rank by carbon emissions per capita
            ranks = self.to_ranks([x["per_capita"] for x in countries])
            question = "Sort these countries by their carbon dioxide emissions per capita."

        user_rankings = []

        for n in range(len(countries)):
            country = countries[n]
            user_rankings.append(dict(country, rank=None))

        embed = self.rankings_embed(
            question + " Enter your reactions *in order* to place your ranks.",
            user_rankings
        )
        message: discord.Message = await ctx.send(embed=embed)

        reactions = ["🇦", "🇧", "🇨", "🇩", "🇪", "🔄"]

        for reaction in reactions:
            await message.add_reaction(reaction)

        rank_counter = 1

        while rank_counter <= 5:
            reaction, user = await self.bot.wait_for("reaction_add")

            if user == self.bot.user:
                continue

            try:
                index = reactions.index(reaction.emoji)
            except ValueError:
                continue

            if index == 5:
                # User clicked refresh button
                for country in user_rankings:
                    country["rank"] = None
                    rank_counter = 1
            else:
                country = user_rankings[index]
                print(country)

                if country["rank"] is None:
                    country["rank"] = rank_counter
                    rank_counter += 1

            embed = self.rankings_embed(
                question + " Enter your reactions *in order* to place your ranks.",
                user_rankings
            )
            await message.edit(embed=embed)

        await ctx.send(f"The correct ranks were: {', '.join(['ABCDE'[x] for x in ranks])}")

        correct = 0

        for n in range(len(user_rankings)):
            country = user_rankings[n]

            if country["rank"] == ranks[n]:
                correct += 1

        if correct == 0:
            final_message = (
                "Unfortunately, you got none of the ranks correct. "
                "Better luck next time!"
            )
        elif correct == 5:
            final_message = "Congratulations! You got all of the ranks correct."
        else:
            final_message = f"You only got {correct} ranks correct. Better luck next time!"

        await ctx.send(final_message)


def setup(bot):
    bot.add_cog(Rankings(bot))
