import requests
import json
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Streams write"

    def handle(self, *args, **options):
        r = requests.get("https://iptv-org.github.io/api/streams.json")

        with open("data/streams.json", "w+") as f:
            data = json.dumps(r.json())
            f.write(data)


# import requests
# import json


# def read():
#     with open("streams.json","r") as f:
#         content = f.read()
#         data = json.loads(content)
#         streams = list(filter(lambda x: x["channel"]=="WUSADT1.us",data))
#         print(streams)
# read()
