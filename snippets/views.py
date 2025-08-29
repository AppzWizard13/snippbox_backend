from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


from .models import Snippet, Tag


class SnippetOverviewAPIView(APIView):
    """
    Overview API:
    Returns total count of user's snippets along with a list of snippets.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        snippets = Snippet.objects.filter(created_by=request.user).prefetch_related("tags")
        data = {
            "total_snippets": snippets.count(),
            "snippets": [
                {
                    "id": snippet.id,
                    "title": snippet.title,
                    "tags": [tag.title for tag in snippet.tags.all()],
                }
                for snippet in snippets
            ]
        }
        return Response(data)


class SnippetCreateAPIView(APIView):
    """
    Create API:
    Create a snippet with title, note, and tags. Reuses tags if they exist.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        title = request.data.get("title")
        note = request.data.get("note")
        tag_titles = request.data.get("tags")  

        if not all([title, note, tag_titles]):
            return Response(
                {"error": "title, note, and tags are required fields."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create snippet first
        snippet = Snippet.objects.create(title=title, note=note, created_by=request.user)

        # Handle multiple tags
        tags = []
        for tag_title in tag_titles:
            tag, _ = Tag.objects.get_or_create(title=tag_title)
            tags.append(tag)
        snippet.tags.set(tags) 

        return Response({
            "id": snippet.id,
            "title": snippet.title,
            "note": snippet.note,
            "tags": [tag.title for tag in snippet.tags.all()],
            "created_by": snippet.created_by.username,
            "created_at": snippet.created_at,
            "updated_at": snippet.updated_at,
        }, status=status.HTTP_201_CREATED)

class SnippetDetailAPIView(APIView):
    """
    Detail API:
    Returns the details of a single snippet belonging to the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, snippet_id, *args, **kwargs):
        snippet = get_object_or_404(Snippet, id=snippet_id, created_by=request.user)
        return Response({
            "id": snippet.id,
            "title": snippet.title,
            "note": snippet.note,
            "tags": [tag.title for tag in snippet.tags.all()],
            "created_by": snippet.created_by.username,
            "created_at": snippet.created_at,
            "updated_at": snippet.updated_at,
        }, status=status.HTTP_200_OK)