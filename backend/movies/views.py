from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from movies.models import Actors, Directors, Genres


class FiltersAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        """
        Returns filter options
        """
        filters = {
            'genre': list(Genres.objects.values_list('name', flat=True).order_by('name')),
            'directors': list(Directors.objects.values_list('name', flat=True).order_by('name')),
            'actors': list(Actors.objects.values_list('name', flat=True).order_by('name')),
        }
        return Response(filters)
