import requests
import json
from django.core.management.base import BaseCommand
from ipytv import playlist
from ipytv.channel import IPTVAttr, IPTVChannel


class Command(BaseCommand):
    help = "Streams write"

    def handle(self, *args, **options):
        r = requests.get("https://iptv-org.github.io/api/streams.json")

        with open("data/streams.json", "w+") as f:
            data = json.dumps(r.json())
            f.write(data)
        with open("/Users/pavelmorozov/Downloads/Rus18.m3u", "r") as f:
            r = requests.get("https://iptv-org.github.io/api/streams.json")
            data = r.json()
            content = f.read()
            playlist = playlist.loads(content)
            channels = playlist.get_channels()
            for channel in channels:
                channel_name = (
                    channel.attributes.get("tvg-id")
                    if channel.attributes.get("tvg-id")
                    else channel.name
                )
                channel_url = channel.url
                rus_data = {
                    "channel": channel_name,
                    "url": channel_url,
                    "timeshift": None,
                    "user_agent": None,
                    "http_referrer": None,
                }
                data.append(rus_data)

    with open(
        "/Users/pavelmorozov/PycharmProjects/peru-channels-backend/peru_backend/data/streams.json",
        "r",
    ) as f:
        f.write(json.dumps(data))


# import requests
# import json


# def read():
#     with open("streams.json","r") as f:
#         content = f.read()
#         data = json.loads(content)
#         streams = list(filter(lambda x: x["channel"]=="WUSADT1.us",data))
#         print(streams)
# read()
