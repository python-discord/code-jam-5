import aiohttp
import asyncio
from discord.ext import commands
import env.config

bot = commands.Bot('!')

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, 'http://0.0.0.0:8080//echo')
        print(html)
    bot.run(env.config.token)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
