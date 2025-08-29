from django.urls import path
from .views import SnippetOverviewAPIView

urlpatterns = [
    path("overview/", SnippetOverviewAPIView.as_view(), name="snippet-overview"),
]