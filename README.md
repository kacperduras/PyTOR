# PyTOR
PyTOR is a small library that allows you to easily download a list of [official TOR output servers](https://check.torproject.org/exit-addresses), and return it in a convenient and accessible way.

#### Installation
```
pip install git+git://github.com/kacperduras/PyTor.git@master
```

#### Example usage
```python
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
```

# Requirements
Python 3.4+

# License
License is available [here](LICENSE).
