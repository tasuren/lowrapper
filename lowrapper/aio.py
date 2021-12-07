"""# Asynchronous version of lowrapper
This module is an asynchronous version of `lowrapper`.  
Usage does not change much.  
`Client.__request__` returns a coroutine.  
The library used for the request is `aiohttp`.

Attributes
----------
CoroutineResponse : Type[Coroutine[Response, Any, Response]]
    The type of coroutine returned by the `__request__` function.
Response
    `aiohttp.ClientResponse`
request : Callable[[method, url, **kwargs], Coroutine]
    This function makes a request using `aiohttp.ClientSession`."""
# lowrapper - Aio Client

from typing import Coroutine, Generic, TypeVar, Any, Union

from aiohttp import ClientSession, ClientResponse as Response

from .client import Client as SyncClient, Method, Path


CoroutineResponse = Coroutine[Any, Any, Response]
async def request(method: Method, url: str, **kwargs) -> Response:
    session = ClientSession(**kwargs.pop("client_session", {}))
    response = await session.request(method, url, **kwargs)
    await session.close()
    return response


ClientResponseT = TypeVar(
    "ClientResponseT", bound=Union[Response, Any]
)
class Client(Path[ClientResponseT], Generic[ClientResponseT]):
    def __init__(self, path: str = ""):
        self.__default_path = path
        super().__init__(path, self) # type: ignore

    def __request__(
        self, path: Path[ClientResponseT], **kwargs
    ) -> ClientResponseT:
        if "url" not in kwargs:
            kwargs["url"] = path.path
        return request(**kwargs) # type: ignore

    def __getattr__(self, name: str) -> Path[ClientResponseT]:
        return SyncClient.__getattr__(self, name) # type: ignore