from discord.ext import commands
from discord import utils
from aiohttp import web
import os
import asyncio
from env.config import token, cogs


HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=commands.when_mentioned_or('!'), **kwargs)
        for cog in cogs:
            self.load_extension(f'cogs.{cog}')
    async def on_ready(self):
        print('bot ready')
        self.channel = utils.get(self.get_all_channels(), name='codejam5')
        

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    await bot.channel.send(name)
    return web.Response(text=name)


async def wshandle(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    async for msg in ws:
        if msg.type == web.WSMsgType.text:
            await ws.send_str(f'received, {msg.data}')
        elif msg.type == web.WSMsgType.binary:
            await ws.send_bytes(msg.data)
        elif msg.type == web.WSMsgType.close:
            break
        if msg.data:
            await bot.channel.send(msg.data)
    return ws


async def dummy(request):
    return web.Response()


app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/ws', wshandle),
                web.get('/favicon.ico', dummy),
                web.get('/test/{name}', handle)])


runner = web.AppRunner(app)
bot = Bot()


async def webs():
    try:
        await runner.setup()
        site = web.TCPSite(runner, HOST, PORT)
        await site.start()
    except Exception:
        await runner.cleanup()
        raise


bot.loop.create_task(webs())
print('starting bot')


try:
    bot.run(token)
except:  # noqa E722
    loop = asyncio.get_running_loop()
    loop.run_until_complete(bot.close())
    raise
