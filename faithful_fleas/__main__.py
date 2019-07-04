import logging
import os

import discord
from discord.ext import commands


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_prefix(client, message):

    prefixes = os.environ.get("DISCORD_PREFIX")
    return commands.when_mentioned_or(*prefixes)(client, message)


bot = commands.Bot(
    command_prefix=get_prefix,
    description='Faithful Fleas',
    owner_id=os.environ.get('DISCORD_OWNER_ID'),
    case_insensitive=True
)
# use os module insted for cogs.
cogs = [cog for cog in os.listdir("FAITHFUL_FLEAS/cogs") if cog.endswith(".py")]

for cog in cogs:
    bot.load_extension("faithful_fleas.cogs." + os.path.splitext(cog)[0])


@bot.event
async def on_ready():
    logger.info(f'Running as {bot.user.name}')
    logger.info(bot.user.id)
    await bot.change_presence(activity=discord.Game(name='spotify'))

bot.run(os.environ.get('DISCORD_TOKEN'), bot=True, reconnect=True)
