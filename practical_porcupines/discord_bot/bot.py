import discord
from discord.ext import commands
from practical_porcupines.utils import ConfigBot

config_bot = ConfigBot()

bot_client = commands.Bot(command_prefix=config_bot.PREFIX)


@bot_client.event
async def on_ready():
    """
    Runs when client boots
    """

    print(f"{bot_client.user.name} is online with the id of '{bot_client.user.id}'!")
