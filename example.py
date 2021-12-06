# lowrapper - Example of the Animechan API typed low wrapper.

from typing import TypedDict, Callable, Any, List

from lowrapper import Method, Path, Client, request, Response


class Quote(TypedDict):
    "Data of anime quote."
    anime: str
    character: str
    quote: str


def _default(self, **kwargs):
    return self.__request__(self, **kwargs)


class Quotes(Path):
    def anime(self, title: str, page: int = 1, **kwargs) -> List[Quote]:
        "Get quote by anime title."
        kwargs["params"] = {"title": title, "page": page}
        return _default(self, **kwargs)

    def character(self, name: str, page: int = 1, **kwargs) -> List[Quote]:
        "Get quote by anime character name."
        kwargs["params"] = {"name": name, "page": page}
        return _default(self, **kwargs)


class Available(Path):
    anime: Path[List[str]]


class Animechan(Client):
    "The Animechan API wrapper."

    BASE = "https://animechan.vercel.app/api/"
    random: Path[Quote]
    quotes: Quotes
    available: Available

    def __request__(self, path: Path, **kwargs) -> Any:
        kwargs["url"] = f"{kwargs.get('url') or self.BASE}{path.path}"
        response = request(kwargs.pop("method", "GET"), **kwargs)
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    client = Animechan()
    print(client.quotes.character("Kino"))