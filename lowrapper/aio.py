# lowrapper - Aio Client

from typing import Protocol, Coroutine, Callable, Any, Union

from aiohttp import ClientSession, ClientResponse as Response

from . import Client as SyncClient, Method, Path, _BaseRequest


CoroutineResponse = Coroutine[Any, Any, Response]
class _Request(_BaseRequest):
    def __call__(
        self, path: Path[CoroutineResponse], method: Method, *args, **kwargs
    ) -> Union[CoroutineResponse, Any]:
        ...


class Client(Path[CoroutineResponse]):
    def __init__(self, path: str = ""):
        self.__default_path = path
        super().__init__(path, self) # type: ignore

    async def _request(self, method: Method, url: str, **kwargs) -> Response:
        session = ClientSession(**kwargs.pop("client_session", {}))
        response = await session.request(method, url, **kwargs)
        await session.close()
        return response

    __request__: _Request
    def __request__(self, path, method, **kwargs): # type: ignore
        return self._request(method, path.path, **kwargs)

    def __getattr__(self, name: str) -> Path[CoroutineResponse]:
        return SyncClient.__getattr__(self, name) # type: ignore


if __name__ == "__main__":
    from asyncio import run

    async def test():
        client = Client[CoroutineResponse]("https://weather.tsukumijima.net/api/")
        test = await client.aaa("GET")
        return await (await client.forecast("GET", params={"city": 120010})).json()

    print(run(test()))