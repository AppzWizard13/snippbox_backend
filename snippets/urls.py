from django.urls import path
from .views import SnippetOverviewAPIView, SnippetCreateAPIView, SnippetDetailAPIView

urlpatterns = [
    path("overview/", SnippetOverviewAPIView.as_view(), name="snippet-overview"),
    path("create/", SnippetCreateAPIView.as_view(), name="snippet-create"),
    path('detail/<int:snippet_id>/', SnippetDetailAPIView.as_view(), name='snippet-detail'),
]