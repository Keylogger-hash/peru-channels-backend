from django.contrib import admin
from .models import Channel, Category, Feedback, Playlist
# Register your models here.
@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    search_fields = ("name",)

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_filter = ("playlist","category")
    search_fields = ("channel_name",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("category_name",)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    pass


# admin.site.register(Playlist)
# admin.site.register(Channel)
# admin.site.register(Category)
# admin.site.register(Feedback)