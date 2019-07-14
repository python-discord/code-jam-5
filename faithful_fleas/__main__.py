import logging
import os

import discord
from discord.ext import commands


logger = logging.getLogger(__name__)


def get_prefix(client, message):

    prefixes = os.environ.get("DISCORD_PREFIX")
    return commands.when_mentioned_or(*prefixes)(client, message)


class FaithfulBot(commands.Bot):
    """An instance of the bot."""

    def __init__(self):
        super().__init__(command_prefix=get_prefix,
                         description="Climate Bot.")

    async def on_ready(self):

        # list of all the cogs.
        cogs = [cog for cog in os.listdir("FAITHFUL_FLEAS/cogs") if cog.endswith(".py")]

        for cog in cogs:
            try:
                # loading the cogs
                self.load_extension("faithful_fleas.cogs." + os.path.splitext(cog)[0])

            except Exception as e:
                # in case any cog/s did not load.
                logger.error(f"Could not load extension {cog} due to error:\n{e}")

        logger.info(f'Running as {self.user.name} with ID: {self.user.id}')
        await self.change_presence(activity=discord.Game(name='A sunny morning!'))

    def run(self):
        # running the bot.
        super().run(os.environ.get('DISCORD_TOKEN'), bot=True, reconnect=True)


if __name__ == "__main__":
    bot = FaithfulBot()
    bot.run()
