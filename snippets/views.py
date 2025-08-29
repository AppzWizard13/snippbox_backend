from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Snippet


class SnippetOverviewAPIView(APIView):
    """
    Overview API:
    Returns total count of snippets created by the user,
    along with a list of snippets and their detail links.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        snippets = Snippet.objects.filter(created_by=request.user).only("id", "title")

        return Response({
            "total_snippets": snippets.count(),
            "snippets": [
                {
                    "id": snippet.id,
                    "title": snippet.title,
                }
                for snippet in snippets
            ]
        })
