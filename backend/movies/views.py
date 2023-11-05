from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from movies.chart import AvgRatingPerGenre, MovieNumberChart
from movies.models import Actors, Directors, Genres
from movies.utils import total_unique_movies


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


class CardsAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        filters = request.data.get('filters', {})
        unique_movie_count = total_unique_movies(filters)
        movie_by_year = MovieNumberChart(filters=filters).generate()
        avg_rating_per_genre = AvgRatingPerGenre(filters=filters).generate()
        response = {
            'total_movies_count': unique_movie_count,
            'movie_by_year': movie_by_year,
            'avg_rating_by_year': avg_rating_per_genre,
        }
        return Response(response, status=HTTP_200_OK)
