from tkinter import *
from tkinter import messagebox
import asyncio
import threading
import random
import os
import aiohttp
from functools import partial
import signal
import sys


HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))
URL = f'http://{HOST}:{PORT}/ws'

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
if sys.platform == 'linux':
    signal.pause()

def _asyncio_thread(root, loop):
    loop.run_until_complete(connect(root))


def do_tasks(root, loop):
    """ Button-Event-Handler starting the asyncio part. """
    threading.Thread(target=_asyncio_thread, args=(root, loop)).start()


async def connect(root):
    session = aiohttp.ClientSession()
    async with session.ws_connect(URL) as ws:
        await ws_send(ws, root)
        async for msg in ws:
            await ws_send(ws, root)
            if msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                break
            await asyncio.sleep(5)
    return
                

async def ws_send(ws, root):
    new_msg_to_send = root.entry.get()
    root.entry.delete(0, 'end')
    if new_msg_to_send == 'exit':
        raise SystemExit(0)
    await ws.send_str(new_msg_to_send)


def main(loop):
    root.entry = Entry(root)
    root.entry.pack()
    Button(master=root, text='Start Posting', command=partial(do_tasks, root, loop)).pack()
    root.mainloop()

if __name__ == '__main__':
    root = Tk()
    try:
        loop = asyncio.get_event_loop()
        print('Press Ctrl+C to exit')
        main(loop)
    except:
        pass
    finally:
        root.entry.config(text='exit')
        do_tasks(root, loop)