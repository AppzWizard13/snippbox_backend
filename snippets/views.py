from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Snippet, Tag


class SnippetOverviewAPIView(APIView):
    """
    Overview API:
    Returns total count of user's snippets along with a list of snippets.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        snippets = Snippet.objects.filter(
            created_by=request.user
        ).prefetch_related("tags")
        data = {
            "total_snippets": snippets.count(),
            "snippets": [
                {
                    "id": snippet.id,
                    "title": snippet.title,
                    "tags": [tag.title for tag in snippet.tags.all()],
                }
                for snippet in snippets
            ],
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
        snippet = Snippet.objects.create(
            title=title, note=note, created_by=request.user
        )

        # Handle multiple tags
        tags = []
        for tag_title in tag_titles:
            tag, _ = Tag.objects.get_or_create(title=tag_title)
            tags.append(tag)
        snippet.tags.set(tags)

        return Response(
            {
                "id": snippet.id,
                "title": snippet.title,
                "note": snippet.note,
                "tags": [tag.title for tag in snippet.tags.all()],
                "created_by": snippet.created_by.username,
                "created_at": snippet.created_at,
                "updated_at": snippet.updated_at,
            },
            status=status.HTTP_201_CREATED,
        )


class SnippetDetailAPIView(APIView):
    """
    Detail API:
    Returns the details of single snippet belonging to the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, snippet_id, *args, **kwargs):
        snippet = get_object_or_404(
            Snippet, id=snippet_id, created_by=request.user
        )
        return Response(
            {
                "id": snippet.id,
                "title": snippet.title,
                "note": snippet.note,
                "tags": [tag.title for tag in snippet.tags.all()],
                "created_by": snippet.created_by.username,
                "created_at": snippet.created_at,
                "updated_at": snippet.updated_at,
            },
            status=status.HTTP_200_OK,
        )


class SnippetUpdateAPIView(APIView):
    """
    Update API:
    Update a snippet's title, note, and tags.
    Only the creator can update their snippet.
    """

    permission_classes = [IsAuthenticated]

    def put(self, request, snippet_id, *args, **kwargs):
        try:
            snippet = Snippet.objects.get(
                id=snippet_id, created_by=request.user
            )
        except Snippet.DoesNotExist:
            return Response(
                {
                    "error": "Snippet not found or you don't have permission to update it."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        title = request.data.get("title")
        note = request.data.get("note")
        tag_titles = request.data.get("tags")

        if not any([title, note, tag_titles]):
            return Response(
                {
                    "error": "At least one field (title, note, or tags) must be provided."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if title:
            snippet.title = title
        if note:
            snippet.note = note

        # Update tags if provided
        if tag_titles is not None:
            tags = []
            for tag_title in tag_titles:
                tag, _ = Tag.objects.get_or_create(title=tag_title)
                tags.append(tag)
            snippet.tags.set(tags)

        snippet.save()

        return Response(
            {
                "id": snippet.id,
                "title": snippet.title,
                "note": snippet.note,
                "tags": [tag.title for tag in snippet.tags.all()],
                "created_by": snippet.created_by.username,
                "created_at": snippet.created_at,
                "updated_at": snippet.updated_at,
            },
            status=status.HTTP_200_OK,
        )


class SnippetDeleteAPIView(APIView):
    """
    Delete selected snippets and return the list of all available
    snippets created by the current user.
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        snippet_ids = request.data.get("snippet_ids", [])

        if not snippet_ids:
            return Response(
                {"error": "No snippet IDs provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Filter snippets that belong to the current user
        snippets_to_delete = Snippet.objects.filter(
            id__in=snippet_ids, created_by=request.user
        )
        deleted_count = snippets_to_delete.count()
        snippets_to_delete.delete()

        # Return updated list of snippets
        snippets = Snippet.objects.filter(
            created_by=request.user
        ).prefetch_related("tags")
        data = {
            "deleted_count": deleted_count,
            "total_snippets": snippets.count(),
            "snippets": [
                {
                    "id": s.id,
                    "title": s.title,
                    "tags": [tag.title for tag in s.tags.all()],
                }
                for s in snippets
            ],
        }
        return Response(data, status=status.HTTP_200_OK)


class TagListAPIView(APIView):
    """
    Tag List API:
    Returns a list of all tags.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        tags = Tag.objects.all().values("id", "title")
        return Response({"total_tags": tags.count(), "tags": list(tags)})


class TagDetailAPIView(APIView):
    """
    Tag Detail API:
    Returns all snippets linked to a specific tag.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, tag_id, *args, **kwargs):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            return Response(
                {"error": "Tag not found."}, status=status.HTTP_404_NOT_FOUND
            )

        snippets = tag.snippets.filter(
            created_by=request.user
        ).prefetch_related("tags")
        data = {
            "tag": tag.title,
            "total_snippets": snippets.count(),
            "snippets": [
                {
                    "id": snippet.id,
                    "title": snippet.title,
                    "tags": [t.title for t in snippet.tags.all()],
                }
                for snippet in snippets
            ],
        }
        return Response(data)
