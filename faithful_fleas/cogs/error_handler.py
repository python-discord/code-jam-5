import logging

import discord
from discord.ext import commands


logger = logging.getLogger(__name__)


class ErrorHandler(commands.Cog):
    """
    An error handling cog.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Task when an error occurs."""

        if isinstance(error, commands.CommandNotFound):
            return logger.info(f"{ctx.author} used {ctx.message.content} "
                               f"but nothing was found.")

        if isinstance(error, commands.MissingRequiredArgument):
            logger.info(f"{ctx.author} called {ctx.message.content} and "
                        f"triggered MissingRequiredArgument error.")
            return await ctx.send(f"`{error.param}` is a required argument.")

        if isinstance(error, commands.CheckFailure):
            logger.info(f"{ctx.author} called {ctx.message.content} and triggered"
                        f" CheckFailure error.")
            return await ctx.send("You do not have permission to use this command!")

        if isinstance(error, (commands.UserInputError, commands.BadArgument)):
            logger.info(f"{ctx.author} called {ctx.message.content} and triggered"
                        f" UserInputError error.")
            return await ctx.send("Invalid arguments.")

        if isinstance(error, commands.CommandOnCooldown):
            logger.info(f"{ctx.author} called {ctx.message.content} and"
                        f" triggered ComamndOnCooldown error.")
            return await ctx.send(f"Command is on cooldown!"
                                  f" Please retry after `{error.retry_after}`")

        if isinstance(error, commands.BotMissingPermissions):
            logger.info(f"{ctx.author} called {ctx.message.content} and triggered"
                        f" BotMissingPermissions error.")
            embed = discord.Embed()
            embed.colour = discord.Colour.blue()
            title = "The bot lacks the following permissions to execute the command:"
            embed.title = title
            embed.description = ""
            for perm in error.missing_perms:
                embed.description += str(perm)
            return await ctx.send(embed=embed)

        if isinstance(error, commands.DisabledCommand):
            logger.info(f"{ctx.author} called {ctx.message.content} and"
                        f" triggered DisabledCommand error.")
            return await ctx.send("The command has been disabled!")

        logger.warning(f"{ctx.author} called {ctx.message.content} and"
                       f" triggered the following error:\n {error}")


def setup(bot):
    """
    Our function called to add the cog to our bot.
    """
    bot.add_cog(ErrorHandler(bot))
    logger.info("ErrorHandler cog loaded")
