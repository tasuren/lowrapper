# lowrapper - Aio lowrapper Client

from typing import Any, Optional

from asyncio import AbstractEventLoop
from aiohttp import ClientSession, ClientResponse

from . import Method, Path, Client as SyncClient, CoroutineResponse


class Client(SyncClient):
    async def _request(self, path: Path, method: Method, **kwargs) -> ClientResponse:
        async with ClientSession() as session:
            return await session.request(
                self._method(method), **self.adjustment(path, **kwargs)
            )

    def request(
        self, path: Path, method: Method, **kwargs
    ) -> CoroutineResponse:
        return self._request(path, method, **kwargs)

    def __getattr__(self, name: str) -> Path:
        return Path(f"{name}/", self)