import asyncio
import threading as th

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .message_handler import MessageHandler


class MessageHandlerThread(th.Thread):
    """
    This class describes a synchronous wrapper thread for the
    `MessageHandler` class.

    It runs the handler in its own event loop.
    """

    def __init__(self, handler: 'MessageHandler'):
        super().__init__()

        self.handler = handler
        """
        The message handler operating inside this thread.
        """

        self.event_loop = asyncio.new_event_loop()
        """
        The asyncio event loop inside which the message handler 
        is working.
        """

    def run(self) -> None:
        self.event_loop.run_until_complete(
            self.handler.inbox_loop()
        )
