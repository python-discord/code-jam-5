import aiohttp
import discord
import logging

from pathlib import Path

from discord.ext import commands

from thoughtful_termites.bot import config
from thoughtful_termites.shared.goal_db.db import GoalDB

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

description = "A simple climate bot made for the 5th code jam."
db_path = Path(__file__).parent.parent / 'shared/goal_db/goals.db'

extensions = [
    'cogs.climate_arguments',
    'cogs.hangman',
    'cogs.minesweeper',
    'cogs.reminders',
    'cogs.trivia'
]


class ClimateBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('>'),
                         description=description,
                         case_insensitive=True
                         )
        self.client_id = config.client_id
        self.owner_id = config.owner_id
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.colour = discord.Colour.blurple()

        if db_path.exists():
            self.db = GoalDB.load_from(db_path)
        else:
            self.db = GoalDB.create_new(db_path)

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
        log.info(f'Bot is logged in as {str(self.user)} (ID: {self.user.id}). Prefix is >')

    @property
    def owner(self):
        return self.get_user(self.owner_id)


bot = ClimateBot()
bot.run(config.bot_token)
