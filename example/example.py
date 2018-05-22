import asyncio
from pytor import PyTOR, Callback, Node

pytor = PyTOR()


class ResponseCallback(Callback):
    @asyncio.coroutine
    def call(self, node: Node):
        print(node.address)
        pass


if __name__ == '__main__':
    pytor.start(ResponseCallback())
