import pandas as pd
from django.db.models import Avg, Count, Q

from movies.models import Movies


def get_movie_release_each_year_data(filters):
    combined_filter = get_combined_filters(filters)

    filtered_movies = Movies.objects.filter(combined_filter)

    unique_titles_per_year = filtered_movies.values('release_year').annotate(
        num_unique_titles=Count('title')).order_by('release_year')

    data = list(unique_titles_per_year)
    df = pd.DataFrame(data)
    return df


def get_combined_filters(filters):
    genre_names = filters.get('genre', [])
    actor_names = filters.get('actors', [])
    director_names = filters.get('directors', [])

    combined_filter = Q()

    if genre_names:
        combined_filter &= Q(genre__name__in=genre_names)

    if actor_names:
        combined_filter &= Q(actors__name__in=actor_names)

    if director_names:
        combined_filter &= Q(directors__name__in=director_names)

    return combined_filter


def get_avg_rating_data(filters):
    combined_filter = get_combined_filters(filters)
    average_rating_per_genre = Movies.objects.filter(combined_filter).values('genre__name', 'release_year').annotate(
        avg_rating=Avg('rating')
    ).order_by('genre__name', 'release_year')

    data = list(average_rating_per_genre)
    df = pd.DataFrame(data)
    df.rename(columns={
        'avg_rating': 'Avg Rating', 'genre__name': 'Genre', 'release_year': 'Release Year'},
        inplace=True)
    df = df[['Avg Rating', 'Release Year', 'Genre']]

    return df


def total_unique_movies(filters):
    combined_filter = get_combined_filters(filters)

    filtered_movies = Movies.objects.filter(combined_filter)

    total_unique_movies_ = filtered_movies.values('title').distinct().count()

    return total_unique_movies_
