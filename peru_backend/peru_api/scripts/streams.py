import requests
import json


def write():
    r = requests.get("https://iptv-org.github.io/api/streams.json")

    with open("streams.json", "w+") as f:
        data = json.dumps(r.json())
        f.write(data)


def read():
    with open("streams.json", "r") as f:
        content = f.read()
        data = json.loads(content)
        streams = list(filter(lambda x: x["channel"] == "WUSADT1.us", data))
        print(streams)


read()
