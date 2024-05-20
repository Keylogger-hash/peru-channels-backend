from rest_framework import serializers
from .models import Channel, Feedback, Category, Playlist
from django_countries.serializers import CountryFieldMixin
from django_countries.fields import CountryField



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ["id","name"]

class ChannelSerializer(CountryFieldMixin, serializers.ModelSerializer):
    playlist = PlaylistSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True, source='category')

    class Meta:
        model = Channel
        exclude = ['category']

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"




class CountrySerializer(serializers.Serializer):
    country = CountryField()