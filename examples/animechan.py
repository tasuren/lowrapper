# lowrapper - Example of the Animechan API typed low wrapper.

from typing import TypedDict, NewType, Callable, Any, List

from lowrapper import Method, Path, Client
from requests import request, Response


AnimeTitle = NewType("AnimeTitle", str)
CharacterName = NewType("CharacterName", str)
QuoteText = NewType("QuoteText", str)
class Quote(TypedDict):
    "Data of anime quote."
    anime: AnimeTitle
    character: CharacterName
    quote: QuoteText


class Quotes(Path[dict]):
    def anime(self, title: str, page: int = 1, **kwargs) -> List[Quote]:
        "Get quote by anime title."
        kwargs["params"] = {"title": title, "page": page}
        return self.__request__(self, **kwargs)

    def character(self, name: str, page: int = 1, **kwargs) -> List[Quote]:
        "Get quote by anime character name."
        kwargs["params"] = {"name": name, "page": page}
        return self.__request__(self, **kwargs)


class Available(Path[dict]):
    anime: Path[List[AnimeTitle]]


class Animechan(Client[dict]):
    "The Animechan API wrapper."

    BASE = "https://animechan.vercel.app/api/"
    random: Path[Quote]
    quotes: Quotes
    available: Available

    def __request__(self, path: Path[dict], **kwargs) -> dict:
        kwargs["url"] = f"{kwargs.get('url') or self.BASE}{path.path}"
        response = request(kwargs.pop("method", "GET"), **kwargs)
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    client = Animechan()
    print(client.random())