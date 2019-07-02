from .message import Message
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .request import Request


class Response(Message):
    """
    This class represents response message objects.

    These are only sent when a request message is received.
    """

    def __init__(self, request: 'Request'):
        super().__init__()

        self.request: 'Request' = None
        """
        The request that asked for this response. 
        Only available on the receiver's side.

        This value is set automatically for the receiver.
        Do not set it for the sender, it'll be ignored.
        """

        self.request_id = request.id
        """
        The ID of the request that asked for this response.
        
        This value must be set before the response is sent.
        """

    def __getstate__(self):
        state = super().__getstate__()
        state['request_id'] = self.request_id
        return state

    def __setstate__(self, state):
        super().__setstate__(state)
        self.request_id = state['request_id']
