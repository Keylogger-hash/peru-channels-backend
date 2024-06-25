import requests
import json
from django.core.management.base import BaseCommand
from peru_api.models import Channel, Category, Playlist
from ipytv import playlist
from ipytv.channel import IPTVChannel
from django.conf import settings
import dataclasses
import typing


@dataclasses.dataclass
class ChannelDTO:
    channel_id: str
    channel_name: str
    channel_url: str
    channel_category: str
    channel_logo: str


class ChannelCategoryName:
    def __init__(self, category_name):
        self.category_name = category_name

    @staticmethod
    def to_lower(category):
        return category.lower().strip()

    def convert(self) -> typing.List[str]:
        category_list = []
        if self.category_name:
            if self.category_name.__contains__(";"):
                split_channel_categories = self.category_name.split(";")
                for category_name in split_channel_categories:
                    category_list.append(category_name)
            else:
                category_list.append(self.category_name)
            return category_list
        return ["undefined"]

    def convert_to_lower(self) -> typing.List[str]:
        category_list = []
        if self.category_name:
            self.category_name = ChannelCategoryName.to_lower(
                self.category_name
            )
            if self.category_name.__contains__(";"):
                split_channel_categories = self.category_name.split(";")
                for category_name in split_channel_categories:
                    category_list.append(category_name)
            else:
                category_list.append(self.category_name)
            return category_list
        return ["undefined"]


class ChannelCategoryPlaylistReader:
    @staticmethod
    def read_unique_categories(channels: typing.List[IPTVChannel]):
        category_set = set()
        for channel in channels:
            channel_category_name = channel.attributes.get("group-title")
            channel_category_obj = ChannelCategoryName(channel_category_name)
            category_list = channel_category_obj.convert()
            for category in category_list:
                category_set.add(category)
        return [
            {
                "category_id": ChannelCategoryName.to_lower(category_name),
                "category_name": category_name,
            }
            for category_name in category_set
        ]


class ChannelCategoryDatabaseReader:
    @staticmethod
    def get_categories_for_insert(categories: typing.List[typing.Dict]):
        category_objects = Category.objects.filter(
            category_id__in=[
                category.get("category_id") for category in categories
            ]
        )
        categories_which_exists = [
            category_obj.category_id for category_obj in category_objects
        ]
        categories_for_insert = None
        if categories_which_exists:
            categories_for_insert = list(
                filter(
                    lambda x: x.get("category_id")
                    not in categories_which_exists,
                    categories,
                )
            )
        else:
            categories_for_insert = categories
        return categories_for_insert


class ChannelCategoryDataSeeder:
    def __init__(self, categories: typing.List[typing.Dict]):
        self.categories = categories

    def insert_categories(self):
        categories_for_insert = (
            ChannelCategoryDatabaseReader.get_categories_for_insert(
                self.categories
            )
        )
        Category.objects.bulk_create(
            [
                Category(
                    category_id=category.get("category_id"),
                    category_name=category.get("category_name"),
                )
                for category in categories_for_insert
            ]
        )


class PlaylistEmptyError(Exception):
    """Exception raised for errors if playlist database empty.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Playlist database empty"):
        self.message = message
        super().__init__(self.message)


class PlaylistDatabaseReader:
    @staticmethod
    def read_playlists_from_database() -> Playlist:
        streams = Playlist.objects.all()
        if not streams:
            raise PlaylistEmptyError()
        return streams

    @staticmethod
    def insert_playlist_into_database():
        with open("data/streams.json", "r+") as f:
            content = f.read()
            print(content)
            streams_data = json.loads(content)
            for stream in streams_data:
                print(streams_data)
                Playlist.objects.create(name=stream.get("name"), url=stream.get('url'))


class PlaylistIPTVReader:
    @staticmethod
    def read_channels_from_source_playlist(
        playlist_from_database: Playlist,
    ) -> typing.List[IPTVChannel]:
        url = playlist_from_database.url
        try:
            playlist_from_source = playlist.loadu(url)
        except Exception as e:
            raise e
        channels = playlist_from_source.get_channels()
        return channels


class ChannelDataSeeder:
    def __init__(self, playlist: Playlist, channels: typing.List[IPTVChannel]):
        self.channels = channels
        self.playlist = playlist

    @staticmethod
    def convert_channel_to_dto(channel) -> typing.List[ChannelDTO]:
        channel_id = (
            channel.attributes.get("tvg-id")
            if channel.attributes.get("tvg-id")
            else channel.name
        )
        channel_name = channel.name
        if channel.name:
            channel_url = channel.url
            channel_category = channel.attributes.get("group-title")
            channel_category = ChannelCategoryName(
                channel_category
            ).convert_to_lower()
            channel_logo = channel.attributes.get("tvg-logo")
            channel_object_dto = ChannelDTO(
                channel_id,
                channel_name,
                channel_url,
                channel_category,
                channel_logo,
            )
            return channel_object_dto
        return None

    def _read_playlist_channels(self) -> typing.List[ChannelDTO]:
        channels_data = []
        for channel in self.channels:
            channel_object_dto = self.convert_channel_to_dto(channel)
            if channel_object_dto is not None:
                channels_data.append(channel_object_dto)
        return channels_data

    def insert_channels(self):
        channels_list = self._read_playlist_channels()
        for channel in channels_list:
            category_objs = Category.objects.filter(
                category_id__in=channel.channel_category
            )
            try:
                print("CHannel",channel.channel_id)
                channel_which_exist = Channel.objects.get(
                    channel_id=channel.channel_id
                )
                if channel.channel_logo != channel_which_exist.logo:
                    channel_which_exist.logo = channel.channel_logo
                if channel.channel_url != channel_which_exist.url:
                    channel_which_exist.url = channel.channel_url
                channel_which_exist.save(update_fields=["logo", "url"])
            except Exception as e:
                channel_obj = Channel.objects.create(
                    channel_id=channel.channel_id,
                    channel_name=channel.channel_name,
                    url=channel.channel_url,
                    playlist=self.playlist,
                    logo=channel.channel_logo,
                )
                channel_obj.category.add(*category_objs)


class DataFillingFacade:

    @staticmethod
    def insert_data():
        playlists_from_database = (
            PlaylistDatabaseReader.read_playlists_from_database()
        )
        if not playlists_from_database:
            PlaylistDatabaseReader.insert_playlist_into_database()
        for stream in playlists_from_database:
            print(stream)
            channels_ipytv = (
                PlaylistIPTVReader.read_channels_from_source_playlist(stream)
            )
            unique_categories = (
                ChannelCategoryPlaylistReader.read_unique_categories(
                    channels_ipytv
                )
            )
            ChannelCategoryDataSeeder(unique_categories).insert_categories()
            channel_data_seader = ChannelDataSeeder(stream, channels_ipytv)
            channel_data_seader.insert_channels()


class Command(BaseCommand):
    help = "Init data from playlist sources"

    def handle(self, *args, **options):
        data_filling_facade = DataFillingFacade()
        data_filling_facade.insert_data()
