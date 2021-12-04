# lowrapper's example - The animechan API low typed wrapper

from typing import TypedDict

from lowrapper import Method, Path, Client, request, Response


BASE = "https://animechan.vercel.app/api/"


class Quotes(Path[dict]):
    def anime(self, title: str, **kwargs) -> dict:
        kwargs["params"] = {"title": title}
        return self.client.request(self, "GET", **kwargs)

    def character(self, name: str, **kwargs):
        kwargs["params"] = {"name": name}
        return self.client.request(self, "GET", **kwargs)


class Available(Path):
    anime: Path[dict]


class AnimeChan(Client[dict]):

    random: Path[dict]
    quotes: Quotes
    available: Available

    def request(self, path: Path, method: Method, **kwargs) -> dict:
        kwargs["url"] = f"{kwargs.get('url') or BASE}{path.path}"
        return request(method, **kwargs).json()


if __name__ == "__main__":
    client = AnimeChan()
    print(client.quotes.anime("keion"))