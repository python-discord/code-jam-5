import aiohttp
import discord
import logging

from discord.ext import commands

from thoughtful_termites.shared.database import get_db
from thoughtful_termites.shared.constants import config_path
from thoughtful_termites.shared.bot_config import Config

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

description = "A simple climate bot made for the 5th code jam."

extensions = [
    'cogs.climate_arguments',
    'cogs.hangman',
    'cogs.treefinder',
    'cogs.rankings',
    'cogs.reminders',
    'cogs.trivia',
    'cogs.farmer_game',
]


class ClimateBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('>'),
                         description=description,
                         case_insensitive=True
                         )

        config = Config.load(config_path)

        self.client_id = config.client_id
        self.owner_id = config.owner_id
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.colour = discord.Colour.blurple()

        self.db = get_db()

        for ext in extensions:
            try:
                self.load_extension(ext)
            except Exception as e:
                print(f'Failed to load {ext}: {e}')

    async def process_commands(self, message):
        ctx = await self.get_context(message)
        ctx.db = self.db
        await self.invoke(ctx)

    async def on_ready(self):
        log.info(
            f'Bot is logged in as {str(self.user)}'
            ' (ID: {self.user.id}). Prefix is >'
        )

    @property
    def owner(self):
        return self.get_user(self.owner_id)


def run():
    config = Config.load(config_path)
    bot = ClimateBot()
    bot.run(config.bot_token)
