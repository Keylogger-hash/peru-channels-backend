import requests
import json


def write():
    r = requests.get("https://iptv-org.github.io/api/channels.json")

    with open("channels.json", "w+") as f:
        data = json.dumps(r.json())
        f.write(data)


def read():
    channels = Channel.objects.all()
    print(channels)


read()
