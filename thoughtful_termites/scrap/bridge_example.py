import asyncio
import multiprocessing as mp
import time

from thoughtful_termites.bridge import (
    Response,
    Request,
    MessageHandler,
)


class ExampleRequest(Request):
    async def on_received(self, handler: 'MessageHandler'):
        print(handler.name, '-', 'request received:', self)

        response = ExampleResponse(self)
        response.message = eval(self.message)

        await handler.send_message_async(response)

        print('\t', 'response sent:', response)

    async def on_response(self, response: Response, handler: MessageHandler):
        print(handler.name, '-', 'response received:', response)
        print('\t', 'in response to:', self)
        print()

    @property
    def message(self):
        return self.content.get('message', None)

    @message.setter
    def message(self, value):
        self.content['message'] = value


class ExampleResponse(Response):
    @property
    def message(self):
        return self.content.get('message', None)

    @message.setter
    def message(self, value):
        self.content['message'] = value


class ExampleProcess1Async(mp.Process):
    def __init__(self, inbox: mp.Queue, outbox: mp.Queue):
        super().__init__()

        self.inbox = inbox
        self.outbox = outbox

    def run(self) -> None:
        handler = MessageHandler(
            self.inbox,
            self.outbox,
            'Handler 1'
        )

        async def send_messages():
            while True:
                request = ExampleRequest()
                request.message = '1+1'

                print(handler.name, '-', 'request sent:', request)
                await handler.send_message_async(request)
                await asyncio.sleep(1)

        async def run_loops():
            await asyncio.gather(
                handler.inbox_loop(),
                send_messages(),
            )

        asyncio.run(run_loops())


class ExampleProcess1Sync(mp.Process):
    def __init__(self, inbox: mp.Queue, outbox: mp.Queue):
        super().__init__()

        self.inbox = inbox
        self.outbox = outbox

    def run(self) -> None:
        handler = MessageHandler(
            self.inbox,
            self.outbox,
            'Handler 1'
        )

        handler_thread = handler.get_loop_thread()
        handler_thread.start()

        while True:
            request = ExampleRequest()
            request.message = '1+1'

            print(handler.name, '-', 'request sent:', request)
            handler.send_message(request)
            time.sleep(1)


class ExampleProcess2Async(mp.Process):
    def __init__(self, inbox: mp.Queue, outbox: mp.Queue):
        super().__init__()

        self.inbox = inbox
        self.outbox = outbox

    def run(self) -> None:
        handler = MessageHandler(
            self.inbox,
            self.outbox,
            'Handler 2'
        )

        asyncio.run(handler.inbox_loop())


class ExampleProcess2Sync(mp.Process):
    def __init__(self, inbox: mp.Queue, outbox: mp.Queue):
        super().__init__()

        self.inbox = inbox
        self.outbox = outbox

    def run(self) -> None:
        handler = MessageHandler(
            self.inbox,
            self.outbox,
            'Handler 2'
        )

        handler_thread = handler.get_loop_thread()
        handler_thread.start()
        handler_thread.join()


if __name__ == '__main__':
    def main():
        queue_1 = mp.Queue()
        queue_2 = mp.Queue()

        # process_1 = ExampleProcess1Sync(
        process_1 = ExampleProcess1Async(
            inbox=queue_1,
            outbox=queue_2
        )

        process_2 = ExampleProcess2Sync(
        # process_2 = ExampleProcess2Async(
            inbox=queue_2,
            outbox=queue_1
        )

        process_1.start()
        process_2.start()

        process_1.join()
        process_2.join()

    main()
