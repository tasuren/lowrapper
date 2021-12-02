# lowrapper's example - The animechan API low wrapper

from lowrapper import Client, Path


class Quotes(Path):
    anime: Path
    character: Path


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
    print(client.random("GET"))