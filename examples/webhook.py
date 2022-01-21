from lowrapper import Client, Response

webhook = ""
client: Client[Response] = Client(webhook)
client.forecast(method="POST", json = {"content": "hello world"})
