from django.urls import path

from movies.views import FiltersAPIView

app_name = 'movies'

urlpatterns = [
    path(
        'filters/',
        FiltersAPIView.as_view(),
        name='filter-fetch-view'
    ),
]
