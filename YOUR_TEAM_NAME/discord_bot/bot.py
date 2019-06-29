import discord
from utils import ConfigApi

config_api = ConfigApi()
bot_client = None # This should be discord

API_ENDPOINT = f"{config_api.API_DOMAIN}:{config_api.API_PORT}"
