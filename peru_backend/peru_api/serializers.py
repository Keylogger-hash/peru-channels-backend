from rest_framework import serializers
from .models import Channel, Feedback, Tournament, Category
from django_countries.serializers import CountryFieldMixin


class ChannelSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = "__all__"


class ChannelStreamSerializer(CountryFieldMixin, serializers.ModelSerializer):
    streams = serializers.ListField(
        child=serializers.URLField(), read_only=True
    )

    class Meta:
        model = Channel
        fields = "__all__"


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
