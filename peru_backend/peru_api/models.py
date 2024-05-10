from django.db import models
from django_countries.fields import CountryField

# Create your models here.


class Feedback(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]


class Tournament(models.Model):
    """Лиги и турниры в"""

    start_time = models.DateTimeField()
    country = CountryField()
    stream_name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    tournament_name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]


class Category(models.Model):
    category_id = models.CharField(max_length=255)
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name
    
class Channel(models.Model):
    channel_name = models.CharField(max_length=255)
    channel_id = models.CharField(max_length=255, null=True, default="")
    owners = models.CharField(max_length=255, default="")
    country = CountryField(null=True, default="")
    lang = models.CharField(max_length=255, default="")
    category = models.ManyToManyField(
        Category,
    )
    website = models.URLField(null=True)
    logo = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.channel_name