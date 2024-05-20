from django.contrib import admin
from django.urls import path, include
from .views import (
    ChannelList,
    ChannelDetail,
    FeedbackList,
    FeedbackDetail,
    CategoryDetail,
    CategoryList,
    IndexAPI,
)


urlpatterns = [
    path("", IndexAPI.as_view(), name="index"),
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
]
