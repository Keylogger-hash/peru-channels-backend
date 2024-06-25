from django.db import models
from django_countries.fields import CountryField

# Create your models here.


class Feedback(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.name


class Category(models.Model):
    category_id = models.CharField(max_length=255)
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name


class Playlist(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Channel(models.Model):
    channel_name = models.CharField(max_length=255)
    channel_id = models.CharField(max_length=255, null=True, default="")
    category = models.ManyToManyField(
        Category,
    )
    url = models.URLField(null=True, blank=True)
    playlist = models.ForeignKey(
        Playlist, on_delete=models.CASCADE, null=True, blank=True
    )
    logo = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["channel_name"]

    def __str__(self):
        return self.channel_name
