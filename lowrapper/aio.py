# lowrapper - Aio Client

from typing import overload, Generic, Coroutine, TypeVar, Callable, Any, Union

from aiohttp import ClientSession, ClientResponse as Response

from .client import Client as SyncClient, Method, Path


async def request(method: Method, url: str, **kwargs) -> Response:
    session = ClientSession(**kwargs.pop("client_session", {}))
    response = await session.request(method, url, **kwargs)
    await session.close()
    return response


ClientResponseT = TypeVar(
    "ClientResponseT", Coroutine[Response, Any, Response], Any
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
        return request(**kwargs)

    def __getattr__(self, name: str) -> Path[ClientResponseT]:
        return SyncClient.__getattr__(self, name, super()) # type: ignore