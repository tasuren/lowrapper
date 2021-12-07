# Asynchronous lowrapper

from lowrapper.aio import Client, CoroutineResponse
from asyncio import run

async def test():
    client = Client[CoroutineResponse]("https://weather.tsukumijima.net/api/")
    response = await client.forecast(method="GET", params={"city": 120010})
    return await response.json(content_type="text/html")

print(run(test()))