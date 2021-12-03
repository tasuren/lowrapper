# lowrapper's example - The animechan API low typed wrapper

from typing import TypedDict

from lowrapper import Method, Path, Client, Response


class AnimeParams(TypedDict, total=False):
    title: str


class CharacterParams(TypedDict, total=False):
    name: str


class Quotes(Path):
    def anime(
        self, method: Method, params: AnimeParams = {}, **kwargs
    ) -> Response: ...

    def character(
        self, method: Method, params: CharacterParams = {}, **kwargs
    ) -> Response: ...


class Available(Path):
    anime: Path


class AnimeChan(Client):

    random: Path
    quotes: Quotes
    available: Available

    def __init__(self, base: str = "https://animechan.vercel.app/api/"):
        self.base = base
        super().__init__()

    def adjustment(self, path: Path, **kwargs) -> dict:
        kwargs["url"] = f"{kwargs.get('url') or self.base}{path.path}"
        return kwargs


if __name__ == "__main__":
    client = AnimeChan()
    print(client.random("GET").json())