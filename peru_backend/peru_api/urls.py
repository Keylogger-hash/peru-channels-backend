from django.contrib import admin
from django.urls import path, include
from .views import (
    ChannelList,
    PlaylistList,
    ChannelDetail,
    FeedbackList,
    FeedbackDetail,
    CategoryDetail,
    CategoryList,
    IndexAPI,
    MainPageAPI
)


urlpatterns = [
    path("", IndexAPI.as_view(), name="index"),
    path("live/", MainPageAPI.as_view(), name='live-page'),
    path("channels/", ChannelList.as_view(), name="channel"),
    path("channels/<int:pk>/", ChannelDetail.as_view(), name="channel-detail"),
    path("feedback/", FeedbackList.as_view(), name="feedback"),
    path(
        "feedback/<int:pk>/", FeedbackDetail.as_view(), name="feedback-detail"
    ),
    path("category/", CategoryList.as_view(), name="category"),
    path(
        "category/<int:pk>/", CategoryDetail.as_view(), name="category-detail"
    ),
    path("playlist/", PlaylistList.as_view(), name="playlist"),
]
