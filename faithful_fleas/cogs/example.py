import logging

from discord.ext import commands


logger = logging.getLogger(__name__)


class Example(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        await ctx.send('Testing!')


def setup(bot):
    logger.info('Example cog loaded!')
    bot.add_cog(Example(bot))
