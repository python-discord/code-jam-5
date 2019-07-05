from typing import TYPE_CHECKING

from .message import Message
from .response import Response

if TYPE_CHECKING:
    from .message_handler import MessageHandler


class Request(Message):
    """
    This class represents request message objects.
    """

    async def on_response(
            self,
            response: Response,
            handler: 'MessageHandler'
    ):
        """
        Called when this request is responded to.

        By default calls the response's `on_received` method.

        :param response: The received response.
        :param handler:  The MessageHandler processing the request/response.
        :return:
        """

        await response.on_received(handler)
