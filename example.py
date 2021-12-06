# lowrapper - Example of the Animechan API typed low wrapper.

from typing import TypedDict, Callable, Any, List

from lowrapper import Method, Path, Client
from requests import request, Response


class Quote(TypedDict):
    "Data of anime quote."
    anime: str
    character: str
    quote: str


def _default(self, **kwargs):
    return self.__request__(self, kwargs.pop("method", "GET"), **kwargs)


class Quotes(Path[Response]):
    def anime(self, title: str, page: int = 1, **kwargs) -> List[Quote]:
        "Get quote by anime title."
        kwargs["params"] = {"title": title, "page": page}
        return _default(self, **kwargs)

    def character(self, name: str, page: int = 1, **kwargs) -> List[Quote]:
        "Get quote by anime character name."
        kwargs["params"] = {"name": name, "page": page}
        return _default(self, **kwargs)


class Available(Path[Response]):
    anime: Path[List[str]]


class Animechan(Client):
    "The Animechan API wrapper."

    BASE = "https://animechan.vercel.app/api/"
    random: Path[Quote]
    quotes: Quotes
    available: Available

    def __request__(self, path: Path, method: Method, **kwargs) -> dict:
        kwargs["url"] = f"{kwargs.get('url') or self.BASE}{path.path}"
        response = request(method, **kwargs)
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    client = Animechan()
    print(client.quotes.character("Kino"))