from django.urls import path

from movies.views import CardsAPIView, FiltersAPIView

app_name = 'movies'

urlpatterns = [
    path(
        'filters/',
        FiltersAPIView.as_view(),
        name='filter-fetch-view'
    ),
    path(
        'cards/',
        CardsAPIView.as_view(),
        name='card-fetch-view'
    ),
]
