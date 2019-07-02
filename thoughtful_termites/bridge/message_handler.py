import asyncio
import multiprocessing as mp
import traceback as tb

from concurrent.futures import ThreadPoolExecutor
from typing import Dict, TYPE_CHECKING

from .response import Response
from .request import Request

if TYPE_CHECKING:
    from .message import Message


class MessageHandler:
    """
    This class describes message handler objects. They handle sending
    message objects and processing responses to request message objects.

    To use a message handler in an async event loop, run the
    `inbox_loop` coroutine.

    To use a message handler in a synchronous program, use
    `get_loop_thread` to get a Thread set up to run the `inbox_loop`.

    To terminate a message handler's inbox loop, place `None` into its
    `inbox`.
    """

    def __init__(
            self,
            inbox: mp.Queue = None,
            outbox: mp.Queue = None,
            name='Handler',
    ):
        if inbox is None:
            inbox = mp.Queue()

        if outbox is None:
            outbox = mp.Queue()

        self.inbox: mp.Queue = inbox
        """Inbox queue. Received messages arrive here."""

        self.outbox: mp.Queue = outbox
        """Outbox queue. Sent messages are placed here."""

        self.name = name
        """Handler name"""

        self.awaiting_response: Dict[..., Request] = dict()
        """
        Map of requests awaiting a response.
        
        key: value = request id: request
        """

    async def inbox_loop(self):
        """
        Runs a loop that takes messages from `inbox` as they arrive
        then processes them.

        :return: None
        """
        event_loop = asyncio.get_event_loop()
        executor = ThreadPoolExecutor(max_workers=1)

        while True:
            message: Message = await event_loop.run_in_executor(
                executor, self.inbox.get
            )

            if message is None:
                break

            if isinstance(message, Response):
                await self._process_response(message)
            else:
                await self._process_message(message)

    def send_message(self, message: 'Message'):
        """
        Sends a message by placing it in the outbox queue.

        If message is a request, places it in the `awaiting_response`
        map.

        :param message: Message to be sent.
        :return: None
        """
        if isinstance(message, Request):
            self.awaiting_response[message.id] = message

        self.outbox.put_nowait(message)

    async def send_message_async(self, message: 'Message'):
        self.send_message(message)

    async def _process_response(self, response: Response):
        """
        Called during `inbox_loop` to handle a message which is a
        response.

        If there's a request in `awaiting_response` waiting for this
        response, it is removed from `awaiting_response`. The response
        object's `request` variable is then set to the removed request
        The request's `on_response` method is then called with the
        response passed as a parameter.

        If there is no request awaiting this response, the response is
        ignored.

        :param response: Response to process.
        :return: None
        """
        try:
            request = self.awaiting_response.pop(
                response.request_id
            )

        except KeyError:
            return

        try:
            response.request = request
            await request.on_response(response, self)
        except Exception:
            tb.print_exc()

    async def _process_message(self, message: 'Message'):
        """
        Called during `inbox_loop` to handle any message which is not a
        response.

        The message's `on_received` message is called and any uncaught
        exceptions from this are printed out.

        :param message: Message to process.
        :return: None
        """
        try:
            await message.on_received(self)
        except Exception:
            tb.print_exc()

    def get_loop_thread(self):
        """
        :return: A new, unstarted, Thread set up to run the handler's
                inbox loop.
        """

        from .message_handler_thread import MessageHandlerThread
        return MessageHandlerThread(self)
