import aiohttp
import discord
import logging
import traceback

from discord.ext import commands

from thoughtful_termites.bot import config

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

description = "A simple climate bot made for the 5th code jam."


class ClimateBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('>'),
                         description=description,
                         case_insensitive=True
                         )
        self.client_id = config.client_id
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.colour = discord.Colour.blurple()

    async def on_ready(self):
        log.info(f'Bot is logged in as {str(self.user)} (ID: {self.user.id}). Prefix is >')

    async def on_command_error(self, context, exception):
        original = exception.original
        if not original:
            return
        print(f'In {context.command.qualified_name}:')
        traceback.print_tb(original.__traceback__)


bot = ClimateBot()
bot.run(config.bot_token)
