# lowrapper - Aio lowrapper Client

from typing import Coroutine, Any

from aiohttp import ClientSession, ClientResponse

from . import Method, Path, BaseClient


Response = Coroutine[Any, Any, ClientResponse]


class Client(BaseClient[Response]):
    async def _request(
        self, path: Path, method: Method, **kwargs
    ) -> ClientResponse:
        async with ClientSession() as session:
            return self.adjustment_after(
                await session.request( # type: ignore
                    self._method(method), **self.adjustment_before(path, **kwargs)
                )
            )

    def request(
        self, path: Path, method: Method, **kwargs
    ) -> Response:
        return self._request(path, method, **kwargs)

    def __getattr__(self, name: str) -> Path:
        return Path(f"{name}/", self)