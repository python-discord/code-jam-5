import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .message_handler import MessageHandler


class Message:
    """
    This class represents individual message objects sent
    from one message handler to another.

    They are fully picklable should be sent using
    MessageHandler.send_message`.

    `on_received` should be overridden on all derived types.
    """

    content = dict()
    """Message content."""

    def __init__(self):
        self.id = uuid.uuid4()
        """Unique message id."""

    def __getstate__(self):
        return {
            'content': self.content,
            'id': self.id,
        }

    def __setstate__(self, state):
        self.content = state['content']
        self.id = state['id']

    def __str__(self):
        return str(self.__getstate__())

    async def on_received(
            self,
            handler: 'MessageHandler'
    ) -> None:
        """
        Callback invoked when `handler` receives this message.

        It should be overridden for all derived `Message` types.

        :param handler: Message handler that received this message.
        :return: None
        """
        raise NotImplementedError
