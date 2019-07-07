import aiohttp
import asyncio
import discord
import logging

import multiprocessing as mp

from pathlib import Path

from discord.ext import commands

from thoughtful_termites.bridge import (
    Response,
    Request,
    MessageHandler,
)
from thoughtful_termites.bot import config
from thoughtful_termites.shared.goal_db.db import GoalDB

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

description = "A simple climate bot made for the 5th code jam."
db_path = Path(__file__).parent.parent / 'shared/goal_db/goals.db'

extensions = [
    'cogs.climate_arguments',
    'cogs.hangman',
    'cogs.treefinder',
    'cogs.rankings',
    'cogs.reminders',
    'cogs.trivia',
    'cogs.farmer_game'
]


class ExampleRequest(Request):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_received(self, handler: 'MessageHandler'):
        # print(handler.name, '-', 'request received:', self)
        #
        # response = ExampleResponse(self)
        # response.message = eval(self.message)
        #
        # await handler.send_message_async(response)
        #
        # print('\t', 'response sent:', response)
        self.bot.dispatch(self.message)
        log.debug('Received message: %s - %s', handler.name, self)

    async def on_response(self, response: Response, handler: MessageHandler):
        # print(handler.name, '-', 'response received:', response)
        # print('\t', 'in response to:', self)
        # print()
        log.debug('Response received: %s - %s', handler.name, response)
        pass

    @property
    def message(self):
        return self.content.get('message', None)

    @message.setter
    def message(self, value):
        self.content['message'] = value


class ExampleResponse(Response):
    @property
    def message(self):
        return self.content.get('message', None)

    @message.setter
    def message(self, value):
        self.content['message'] = value

    async def on_received(
            self,
            handler: 'MessageHandler'
    ):
        return


class BotBridgedProcessAsync(mp.Process):
    def __init__(self, inbox: mp.Queue, outbox: mp.Queue, bot: commands.Bot):
        super().__init__()

        self.inbox = inbox
        self.outbox = outbox
        self.bot = bot

    def run(self) -> None:
        handler = MessageHandler(
            self.inbox,
            self.outbox,
            'Bot Handler'
        )

        async def send_messages():
            # while True:
            #     request = ExampleRequest(self.bot)
            #     request.message = '1+1'
            #
            #     print(handler.name, '-', 'request sent:', request)
            #     await handler.send_message_async(request)
            #     await asyncio.sleep(1)
            return

        async def run_loops():
            # await asyncio.gather(
            #     handler.inbox_loop(),
            #     send_messages(),
            # )
            await handler.inbox_loop()

        asyncio.run(run_loops())


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
