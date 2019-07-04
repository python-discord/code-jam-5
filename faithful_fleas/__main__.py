import logging
import os

import discord
from discord.ext import commands


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
    try:
        bot.load_extension("faithful_fleas.cogs." + os.path.splitext(cog)[0])
    except Exception as e:
        logger.error(f"Could not load extension {cog} due to error: {e}")


@bot.event
async def on_ready():
    logger.info(f'Running as {bot.user.name}')
    logger.info(f"ID: {bot.user.id}")
    await bot.change_presence(activity=discord.Game(name='A sunny morning!'))

bot.run(os.environ.get('DISCORD_TOKEN'), bot=True, reconnect=True)
