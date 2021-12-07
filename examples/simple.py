# 天気予報 API the low level wrapper

from lowrapper import Client, Response

client: Client[Response] = Client("https://weather.tsukumijima.net/api/")

print(client.forecast(method="GET", params={"city": 120010}).json())