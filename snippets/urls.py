from django.urls import path
from .views import SnippetOverviewAPIView, SnippetCreateAPIView

urlpatterns = [
    path("overview/", SnippetOverviewAPIView.as_view(), name="snippet-overview"),
    path("create/", SnippetCreateAPIView.as_view(), name="snippet-create"),
]