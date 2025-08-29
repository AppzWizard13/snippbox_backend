from django.urls import path
from .views import (
    SnippetOverviewAPIView,
    SnippetCreateAPIView,
    SnippetDetailAPIView,
    SnippetUpdateAPIView,
    SnippetDeleteAPIView,
    TagListAPIView,
)

urlpatterns = [
    path("overview/", SnippetOverviewAPIView.as_view(), name="snippet-overview"),
    path("create/", SnippetCreateAPIView.as_view(), name="snippet-create"),
    path("detail/<int:snippet_id>/", SnippetDetailAPIView.as_view(), name="snippet-detail"),
    path("update/<int:snippet_id>/", SnippetUpdateAPIView.as_view(), name="snippet-update"),
    path("delete/", SnippetDeleteAPIView.as_view(), name="snippet-delete"),
    path("tags/", TagListAPIView.as_view(), name="tag-list"),

]
