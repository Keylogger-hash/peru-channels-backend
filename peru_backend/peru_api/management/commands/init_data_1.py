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
    channel_url:str
    channel_category: str
    channel_logo: str


class ChannelCategory:
    def __init__(self, category_name):
        self.category_name = category_name
    
    @staticmethod
    def to_lower(category):
        return category.lower().strip() 

    def convert(self)->typing.List[str]:
        category_list = []
        if self.category_name:
            if self.category_name.__contains__(';'):
                split_channel_categories = self.category_name.split(';')
                for category_name in split_channel_categories:
                    category_list.append(category_name)
            else:
                category_list.append(self.category_name)
            return category_list
        return ['undefined']
    
    def convert_to_lower(self)->typing.List[str]:
        category_list = []
        if self.category_name:
            self.category_name = ChannelCategory.to_lower(self.category_name)
            if self.category_name.__contains__(';'):
                split_channel_categories = self.category_name.split(';')
                for category_name in split_channel_categories:
                    category_list.append(category_name)
            else:
                category_list.append(self.category_name)
            return category_list
        return ['undefined']

class ChannelCategoryList:
    def __init__(self):
        pass


class PlaylistEmptyError(Exception):
    """Exception raised for errors if playlist database empty.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self,  message="Playlist database empty"):
        self.message = message
        super().__init__(self.message)

def convert_channel_to_dto(channel)->typing.List[ChannelDTO]:
    channel_id = (
        channel.attributes.get("tvg-id")
        if channel.attributes.get("tvg-id")
        else channel.name
    )
    channel_name = channel.name
    if channel.name:
        channel_url = channel.url
        channel_category = channel.attributes.get("group-title")
        channel_category = ChannelCategory(channel_category).convert_to_lower()
        channel_logo = channel.attributes.get("tvg-logo")
        channel_object_dto = ChannelDTO(
            channel_id,
            channel_name,
            channel_url,
            channel_category,
            channel_logo
        )
        return channel_object_dto
    return None

class Command(BaseCommand):
    help = "Init data from different sources"

    def _read_playlists_from_database(self) -> Playlist:
        streams = Playlist.objects.all()
        if streams == []:
            raise PlaylistEmptyError()
        return streams
    
    def _read_source_playlist(self, playlist_from_database: Playlist)->typing.List[IPTVChannel]:
        url = playlist_from_database.url
        try:
            playlist_from_source = playlist.loadu(url)
        except Exception as e:
            raise e
        channels = playlist_from_source.get_channels()
        return channels
    
    def _read_playlist_channels(self,channels: typing.List[IPTVChannel]):
        channels_data = []
        for channel in channels:
            channel_object_dto = convert_channel_to_dto(channel) 
            if channel_object_dto is not None:
                channels_data.append(channel_object_dto)
        return channels_data

    def _read_unique_categories(self,channels: typing.List[IPTVChannel]):
        category_set = set()
        for channel in channels:
            channel_category = channel.attributes.get("group-title")
            channel_category_obj = ChannelCategory(channel_category)
            category_list = channel_category_obj.convert()
            for category in category_list:
                category_set.add(category)
        return [{"category_id":ChannelCategory.to_lower(category_name),"category_name":category_name} for category_name in category_set]
                
    def _insert_channels(self, playlist:Playlist,channels: typing.List[ChannelDTO]):
        for channel in channels:
            category_objs = Category.objects.filter(category_id__in = channel.channel_category)
            try:
                channel_which_exist = Channel.objects.get(channel_id=channel.channel_id)
                if channel.channel_logo != channel_which_exist.logo:
                    channel_which_exist.logo = channel.channel_logo
                if channel.channel_url != channel_which_exist.url:
                    channel_which_exist.url = channel.channel_url
                channel_which_exist.save(update_fields=['logo','url'])
            except Exception as e:
                channel_obj = Channel.objects.create(
                    channel_id = channel.channel_id,
                    channel_name=channel.channel_name,
                    url=channel.channel_url,
                    playlist=playlist,
                    logo=channel.channel_logo
                )
                channel_obj.category.add(*category_objs)
    def _insert_categories(self, categories:typing.List[typing.Dict]):
        category_objects = Category.objects.filter(category_id__in=[category.get('category_id') for category in categories])
        categories_which_exists = [category_obj.category_id for category_obj in category_objects]
        if categories_which_exists:
            categories_for_insert = list(filter(lambda x: x.get('category_id') not in categories_which_exists,categories))
        else:
            categories_for_insert = categories
        Category.objects.bulk_create(
            [
                Category(category_id=category.get('category_id'),category_name=category.get('category_name'))
                for 
                    category
                in categories_for_insert
            ]
        )
    
    def handle(self, *args, **options):
        playlists_from_database = self._read_playlists_from_database()    
        for playlist in  playlists_from_database:
            channels_ipytv = self._read_source_playlist(playlist)  
            unique_categories = self._read_unique_categories(channels_ipytv)
            self._insert_categories(unique_categories)
            channels_dto_objects = self._read_playlist_channels(channels_ipytv)
            self._insert_channels(playlist,channels_dto_objects)