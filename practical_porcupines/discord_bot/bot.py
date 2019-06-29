import discord
from discord.ext import commands
from practical_porcupines.utils import ConfigApi

config_api = ConfigApi()
bot_client = commands.Bot(command_prefix=config_api.PREFIX)

API_ENDPOINT = f"{config_api.API_DOMAIN}:{config_api.API_PORT}"
