import discord
from discord.ext import commands
from practical_porcupines.utils import ConfigBot
from practical_porcupines.discord_bot.api import get_difference
from practical_porcupines.discord_bot.utils import (
    embed_generator,
    decode_diff_resp,
    check_date,
)

config_bot = ConfigBot()

bot_client = commands.Bot(command_prefix=config_bot.PREFIX)


@bot_client.event
async def on_ready():
    """
    Runs when client boots
    """

    print(f"{bot_client.user.name} is online with the id of '{bot_client.user.id}'!")
    print(await decode_diff_resp(await get_difference("2010", "2019")))  # API testing
