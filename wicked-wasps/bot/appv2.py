from discord.ext import commands
from aiohttp import web
import os
from env.config import token

bot = commands.Bot("!")

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
    return ws

async def dummy(request):
    return web.Response()

app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/ws', wshandle),
                web.get('/favicon.ico', dummy),
                web.get('/test/{name}', handle)])
runner = web.AppRunner(app)


async def webs():
  try:
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    bot.channel = bot.get_channel(595032270688092160)
    await site.start()
  except Exception as e:
    print(e)
    await runner.cleanup()
    raise

bot.loop.create_task(webs())
print('starting bot')

try:
  bot.run(token)
except:
  bot.close()
  raise

