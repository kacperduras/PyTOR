# PyTOR
PyTOR is a small library that allows you to easily download a list of [official TOR output servers](https://check.torproject.org/exit-addresses), and return it in a convenient and accessible way.

#### Example usage
```python
from pytor.pytor import *


class ResponseCallback(Callback):
    def call(self, node: Node):
        print(node.address)
        pass

pytor = PyTOR()
pytor.start(ResponseCallback())
```

# Requirements
Python 3.4+

# License
License is available [here](LICENSE).
