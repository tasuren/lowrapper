# lowrapper
The lowrapper is a library for quickly and easily creating an environment for tapping the API without implementation.  
Typing the `Client` class creates a simple API wrapper with type completion.  
Also, it may also be useful for creating API wrappers.  
Let's start by looking at Simple Example below to see how it works.

## Simple Example
This is the [weather forecast API's](https://weather.tsukumijima.net) low wrapper.  
```python
# 天気予報 API the low level wrapper

from lowrapper import Client

client = Client("https://weather.tsukumijima.net/api/")

print(client.forecast("GET", params={"city": 120010}).json())
# [GET] https://weather.tsukumijima.net/api/forecast?city=120010
```
This example uses the weather forecast API to get weather forecast information for Chiba Prefecture.  
(Chiba Prefecture is a prefecture in Japan.)
### Explanation for Simple Example
1. Pass the API endpoint base URL to `Client`.
2. Write the end of the endpoint of the API in the class attribute. (`client.forecast` -> `/forecast`)
3. Hit the API.

## FAQs
**Q: I want to hit an endpoint that changes dynamically.**  
**A:** You can hit this by using like dictionary as follows:  
`client[YOUR_DYNAMIC_ENDPOINT]("GET", ...)`

**Q: I want to type the client class.**  
**A:** You can type by inheriting the client class as follows:
```python
class Endpoint(Path):
    ping: Path[requests.Response]

class Client(lowrapper.Client):
    some: Endpoint

client = Client("https://api.some.web/")
print(client.some.ping("GET").text())
# -> pong
```

## Installation
You can install lowrapper by running this command.  
`pip install lowrapper`