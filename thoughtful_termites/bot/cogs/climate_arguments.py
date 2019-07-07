import datetime
import discord
import json
import random

from discord.ext import commands

from thoughtful_termites.bot.unlocks import has_unlocked
from thoughtful_termites.bot.resources import climate_arguments_path


class ClimateArguments(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        with open(climate_arguments_path) as fp:
            self.raw_climate_arguments = json.load(fp)

    async def cog_command_error(self, ctx, error):
        """Error handler for the cog; returns errors to the user if required.
        """
        if isinstance(error, (commands.BadArgument, commands.MissingRequiredArgument,
                              commands.CheckFailure)
                      ):
            return await ctx.send(str(error))

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
                              timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=f'This was ID No. {argument_id}')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ClimateArguments(bot))
