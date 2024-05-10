import requests
import json
from django.core.management.base import BaseCommand
from peru_api.models import Channel, Category


class Command(BaseCommand):
    help = "Channels write"

    def handle(self, *args, **options):
        r = requests.get("https://iptv-org.github.io/api/channels.json")

        with open("channels.json", "w+") as f:
            data = json.dumps(r.json())
            f.write(data)
        with open("channels.json", "r") as f:
            channels_objects = []
            data = json.loads(f.read())
            for item in data:
                categories = item["categories"]
                category_objects = Category.objects.filter(category_id__in=categories)
                print(categories)
                print(category_objects)
                channel_object = Channel.objects.create(
                    channel_name=item["name"],
                    channel_id=item["id"],
                    owners=";".join(item["owners"]),
                    country=item["country"],
                    lang=",".join(item["languages"]),
                    website=item["website"],
                    logo=item["logo"],
                )
                if category_objects:
                    for category_object in category_objects:
                        channel_object.category.add(category_object)
                #xchannels_objects.append(channel_object)


# def write():
#     r = requests.get("https://iptv-org.github.io/api/channels.json")


#     with open("channels.json", "w+") as f:
#         data = json.dumps(r.json())
#         f.write(data)

# def read():
#     channels = Channel.objects.all()
#     print(channels)
# read()
