import requests
import json
from django.core.management.base import BaseCommand
from peru_api.models import Channel, Category, Playlist
from ipytv import playlist
from django.conf import settings
import dataclasses
import typing

@dataclasses.dataclass
class PlaylistDTO:
    channel_id: int
    playlist_from_database_id: int
    channel_name:str
    channel_url:str
    channel_category: str
    channel_logo: str



class PlaylistEmptyError(Exception):
    """Exception raised for errors if playlist database empty.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self,  message="Playlist database empty"):
        self.message = message
        super().__init__(self.message)

class Command(BaseCommand):
    help = "Init data from different sources"

    def _write_foriegn_streams(self, additional_data=None):
        streams_request = requests.get(
            "https://iptv-org.github.io/api/streams.json"
        )

        with open("data/streams.json", "w+") as f:
            streams_data = streams_request.json()
            if additional_data:
                streams_data.extend(additional_data)
            f.write(json.dumps(streams_data,ensure_ascii=False))

    def _write_foreign_channels(self, additional_data=None):
        channels_request = requests.get(
            "https://iptv-org.github.io/api/channels.json"
        )

        with open(settings.DATA_DIR / "channels.json", "w+") as f:
            channels_data = channels_request.json()
            if additional_data:
                channels_data.extend(additional_data)
            write_data = json.dumps(channels_data,ensure_ascii=False)
            f.write(write_data)

        with open(settings.DATA_DIR / "channels.json", "r") as channels_file:
            data = json.loads(channels_file.read())
            for item in data:
                categories = item["categories"]
                category_objects = Category.objects.filter(
                    category_id__in=categories
                )
                
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

    def _write_foreign_categories(self, additional_data=None):
        categories_request = requests.get(
            "https://iptv-org.github.io/api/categories.json"
        )

        with open(settings.DATA_DIR / "categories.json", "w+") as f:
            categories_data = categories_request.json()
            if additional_data:
                categories_data.extend(additional_data)
            f.write(json.dumps(categories_data,ensure_ascii=False))
        with open(settings.DATA_DIR / "categories.json", "r") as f:
            category_objects = []
            data = json.loads(f.read())
            for item in data:
                category_object = Category(
                    category_id=item["id"], category_name=item["name"]
                )
                category_objects.append(category_object)
            Category.objects.bulk_create(category_objects)

    def _read_playlists_from_database(self) -> Playlist:
        streams = Playlist.objects.all()
        if streams == []:
            raise PlaylistEmptyError()
        return streams
    
    def _read_playlist(self, playlist_from_database: Playlist):
        url = playlist_from_database.url
        playlist_from_database_id = playlist_from_database.id
        try:
            playlist_from_source = playlist.loadu(url)
        except Exception as e:
            raise e
        channels = playlist_from_source.get_channels()
        channels_data = []
        for channel in channels:
            channel_id = (
                channel.attributes.get("tvg-id")
                if channel.attributes.get("tvg-id")
                else channel.name
            )
            channel_name = channel.name
            channel_url = channel.url
            channel_category = channel.attributes.get("group-title")
            channel_category = (
                [channel_category.lower().strip()] if channel_category else ["general"]
            )
            channel_logo = channel.attributes.get("tvg-logo")
            channel_data = {
                "channel_id": channel_id,
                "playlist_id": playlist_from_database_id,
                "channel_name": channel_name,
                "channel_url": channel_url,
                "channel_category": channel_category,
                "channel_logo": channel_logo
            }
            channels_data.append(channel_data)
        return channels_data

    def _insert_channels(self, channels: typing.List[PlaylistDTO]):
        pass
        

    def _read_russian_playlist_streams(self):
        url = "https://spirt007.github.io/Tvru/Rus18.m3u"
        russian_playlist = playlist.loadu(url)
        channels = russian_playlist.get_channels()
        streams_data = []

        for channel in channels:
            channel_id = (
                channel.attributes.get("tvg-id")
                if channel.attributes.get("tvg-id")
                else channel.name
            )
            channel_url = channel.url
            rus_streams_data = {
                "channel": channel_id,
                "url": [channel_url],
                "timeshift": None,
                "user_agent": None,
                "http_referrer": None,
            }
            streams_data.append(rus_streams_data)
        return streams_data

    def _read_russian_playlist_channels(self):
        url = "https://spirt007.github.io/Tvru/Rus18.m3u"
        russian_playlist = playlist.loadu(url)
        channels = russian_playlist.get_channels()
        channels_data = []

        for channel in channels:
            channel_name = channel.name
            channel_id = (
                channel.attributes.get("tvg-id")
                if channel.attributes.get("tvg-id")
                else channel.name
            )
            channel_url = channel.url
            channel_logo = channel.attributes.get("tvg-logo")
            channel_category = channel.attributes.get("group-title")
            channel_category = (
                [channel_category.lower().strip()] if channel_category else ["general"]
            )
            if channel_name != "":
                rus_channels_data = {
                    "id": channel_id,
                    "name": channel_name,
                    "alt_names": [],
                    "network": None,
                    "owners": [],
                    "country": "RU",
                    "subdivision": None,
                    "city": None,
                    "broadcast_area": ["c/DO"],
                    "languages": ["rus"],
                    "categories": channel_category,
                    "is_nsfw": False,
                    "launched": None,
                    "closed": None,
                    "replaced_by": None,
                    "website": "https://example.com",
                    "logo": channel_logo,
                }
            channels_data.append(rus_channels_data)
        return channels_data

    def _read_russian_playlist_category(self):
        url = "https://spirt007.github.io/Tvru/Rus18.m3u"
        russian_playlist = playlist.loadu(url)
        channels = russian_playlist.get_channels()
        category_unique_data = set()

        for channel in channels:
            channel_category = channel.attributes.get("group-title")
            if channel_category:
                channel_category ="Радио" if channel_category == "Радио_radio=_true" else channel_category
                category_unique_data.add(channel_category)

        return [
            {
                "id": category.lower().strip(),
                "name": category,
            }
            for category in category_unique_data
        ]

    def handle(self, *args, **options):
        category = self._read_russian_playlist_category()
        self._write_foreign_categories(additional_data=category)
        streams = self._read_russian_playlist_streams()
        self._write_foriegn_streams(additional_data=streams)
        channels = self._read_russian_playlist_channels()
        self._write_foreign_channels(additional_data=channels)
