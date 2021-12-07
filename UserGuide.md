# User Guide
The User Guide then creates a wrapper around the [Animechan API](https://animechan.vercel.app).
## Make very simple wrapper
First, let's get the famous words of animation characters randomly from Animechan.
```python
client = Client[Response]("https://animechan.vercel.app/api/")
print(client.random(method="GET").json())
```
### Explanation
> `client = Client[Response]("https://animechan.vercel.app/api/")`
Create an instance of the client class based on `https://animechan.vercel.app/api/`.
> `print(client.random(method="GET").json())`
Make a request by appending `random` to the base URL you specified earlier.  
It then prints the returned JSON as a dictionary.

As you can see, `Client` appends the accessed attribute to the endpoint path.  
You can then make a request by invoking that attribute.

## Upgrade very simple wrapper
If you want to make a complete wrapper, adding `GET` each time such as `random `is very troublesome.  
So, you don't have to override the `__request__` that is called at request time to pass methods to arguments.  
In addition, let's make sure that the hit API generates an error such as a 404 error.
```python
from lowrapper import Client, Response, Path, request

class Animechan(Client[dict]):
    def __init__(self):
        super().__init__("https://animechan.vercel.app/api/")

    def __request__(self, path: Path[dict], **kwargs) -> dict:
        kwargs["url"] = path.path
        kwargs["method"] = "GET"
        response = request(**kwargs)
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    client = Animechan()
    print(client.random())
```

## Make full typed wrapper
