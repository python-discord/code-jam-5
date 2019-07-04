import logging

from discord.ext import commands


logger = logging.getLogger(__name__)


class Moderation(commands.Cog):
    """This cog is for moderation commands."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='purge', aliases=['del', 'd', 'p', 'delete'])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        """A command to delete message."""
        # temporary command to keep text channel look neat.
        await ctx.channel.purge(limit=amount, before=ctx.message)
        await ctx.send(f'{amount} messages have been deleted!')


def setup(bot):
    """Moderation cog load."""
    logger.info("Moderation cog loading...")
    bot.add_cog(Moderation(bot))
