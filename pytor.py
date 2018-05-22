import asyncio
import requests
from concurrent.futures import ThreadPoolExecutor

URL = "https://check.torproject.org/exit-addresses"
HEADERS = {"Content-Type": "application/text", "Content-Encoding": "UTF-8"}


class Node:
    def __init__(self, id, published, last_status, address):
        self.id = id
        self.published = published
        self.last_status = last_status
        self.address = address


class Callback:
    @asyncio.coroutine
    def call(self, node: Node):
        pass


class ThreadManager:
    def __init__(self, queue, executor):
        self.queue = queue
        self.executor = executor

    def add_element(self, method):
        if method is not None:
            self.queue.run_until_complete(self._add_element(method))

    def stop(self):
        self.queue.close()

    @asyncio.coroutine
    async def _add_element(self, method):
        if method is not None:
            self.queue.run_in_executor(self.executor, method)


class PyTOR:
    def __init__(self, queue=asyncio.get_event_loop(), executor=ThreadPoolExecutor()):
        self.thread_manager = ThreadManager(queue=queue, executor=executor)

    def start(self, callback: Callback):
        if callback is None:
            pass

        try:
            self.thread_manager.add_element(method=self._start(callback=callback))
        finally:
            self.thread_manager.stop()

    def _start(self, callback: Callback):
        response = None
        queue = asyncio.get_event_loop()

        try:
            response = requests.get(URL, stream=True, headers=HEADERS)
            result = response.raw.data
            if result is None:
                pass

            decoded_result = result.decode("UTF-8")

            node = None
            published = None
            last = None
            address = None

            data = decoded_result.split("\n")
            for target in data:
                array = target.split()
                if len(array) <= 0:
                    continue

                if array[0] == "ExitNode":
                    node = array[1]
                elif array[0] == "Published":
                    published = array[1] + " " + array[2]
                elif array[0] == "LastStatus":
                    last = array[1] + " " + array[2]
                elif array[0] == "ExitAddress":
                    address = array[1]  # only exit-address
                else:
                    raise ValueError("Unknown element: " + array[0])

                if node is None:
                    continue
                if published is None:
                    continue
                if last is None:
                    continue
                if address is None:
                    continue

                queue.run_until_complete(callback.call(Node(id=node, published=published, last_status=last,
                                                       address=address)))

                node = None
                published = None
                last = None
                address = None

        finally:
            if response is not None:
                response.close()

            queue.close()
