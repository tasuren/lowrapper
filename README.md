[![PyPI](https://img.shields.io/pypi/v/lowrapper)](https://pypi.org/project/lowrapper/) ![PyPI - Downloads](https://img.shields.io/pypi/dm/lowrapper) ![PyPI - License](https://img.shields.io/pypi/l/lowrapper) [![document](https://img.shields.io/badge/Documentation-passing-blue)](https://tasuren.github.io/lowrapper/)
# lowrapper
The lowrapper is a library for quickly and easily creating an environment for tapping the API without implementation.  
Typing the `Client` class creates a simple API wrapper with type completion.  
Also, it may also be useful for creating API wrappers.  
Let's start by looking at Simple Example below to see how it works.

## Simple Example
This is the [weather forecast API's](https://weather.tsukumijima.net) low wrapper.  
```python
# 天気予報 API the low level wrapper

from lowrapper import Client, Response

client: Client[Response] = Client("https://weather.tsukumijima.net/api/")

print(client.forecast(method="GET", params={"city": 120010}).json())
# [GET] https://weather.tsukumijima.net/api/forecast?city=120010
```
This example uses the weather forecast API to get weather forecast information for Chiba Prefecture.  
(Chiba Prefecture is a prefecture in Japan.)
### Explanation for Simple Example
1. Pass the API endpoint base URL to `Client`.
2. Write the end of the endpoint of the API in the class attribute. (`client.forecast` -> `/forecast`)
3. Hit the API.

As you can see, you can create an endpoint with Python class attributes.  
You can also change the arguments for the request.  (Let's see [FAQs](#FAQs))

## Installation
You can install lowrapper by running this command.  
`pip install lowrapper`

If you want asynchronous lowrapper, you can get this by running this command.  
`pip install lowrapper[asynchronous]` or `pip install aiohttp`

## FAQs
**Q: I want to hit an endpoint that changes dynamically.**  
**A:** You can hit this by using like dictionary as follows.  
`client[YOUR_DYNAMIC_ENDPOINT]("GET", ...)`

**Q: I want to type the client class.**  
**A:** You can type by inheriting the client class as follows.
```python
from lowrapper import Client, Path, Response

class Endpoint(Path[Response]):
    ping: Path[Response]

class MySomeAPIClient(Client[Response]):
    some: Endpoint

client = MySomeAPIClient("https://api.some.web/")
print(client.some.ping(method="GET").text)
# [GET] https://api.some.web/some/ping
# -> Some's PONG!
```

**Q: I want to use asynchronous version of lowrapper.**  
**A:** You can use it by importing `lowrapper.aio` as follows.
```python
from lowrapper.aio import Client, Path, CoroutineResponse

client: Client[CoroutineResponse] = Client("https://asynchronous.love/")
```
And you should install `aiohttp` to request.

**Q: I want to change the request args.**  
**A:** You can change the request args like bellow.
```python
from lowrapper import Client, Path, Method, Response


class MyClient(Client[Response]):

    BASE = "https://simple.chat/"

    def __init__(self):
        super().__init__(self.BASE)

    def send(self, message: str) -> Response:
        return self.__request__(self, method="POST", json={"content": message})


client = MyClient()
client.send("Hi")
# [POST] https://simple.chat/send
# <Data> {"content": "Hi"}
```

**Q: I want a guide.**  
**A:** Let's see documentation's guide.

## Contributing
Let's cooperate by making an issue and submitting a Pull Request!  
In case of Pull Request, please try not to change the style of the code. (65% PEP8)

## Documentation
UserGuide and Documentation is [here](https://tasuren.github.io/lowrapper/).
