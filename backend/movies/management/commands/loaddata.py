import csv
import os
import re

from django.conf import settings
from django.core.management.commands.loaddata import Command as LoadDataCommand

from movies.models import Movies, Directors, Genres, Actors


class Command(LoadDataCommand):
    help = 'Loads Movies Data from CSV.'

    def add_arguments(self, parser):
        parser.add_argument('option', type=str)

    @staticmethod
    def extract_first_year(text):
        text = re.sub(r'[^\w\s-]', '', text)

        words = text.split()
        for word in words:
            year_match = re.match(r'(\d{4})(?:\D*|$)', word)
            if year_match:
                return int(year_match.group(1))
        return None

    @staticmethod
    def extract_directors_and_actors(text):
        directors, actors = [], []
        directors_text = re.findall(r"Director:\s*(.*)", text)
        actors_text = re.findall(r"Stars:\s*(.*)", text)

        if directors_text:
            directors = [director.strip() for director in directors_text[0].split(",")]

        if actors_text:
            actors = [actor.strip() for actor in actors_text[0].split(",")]
        return directors, actors

    @staticmethod
    def add_multi_entity(entities, entity_model):
        entity_to_add = []
        for entity in entities:
            if entity.strip():
                entity_to_add.append(entity_model.objects.get_or_create(name=entity.strip())[0])
        return entity_to_add

    def load_movies(self):
        csv_file_path = os.path.join(settings.BASE_DIR, 'csv', 'movies.csv')

        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                if row['YEAR']:
                    release_year = self.extract_first_year(row['YEAR'])
                    if release_year:
                        rating = float(row['RATING']) if row['RATING'] else 0

                        movie = Movies.objects.create(
                            title=row['MOVIES'],
                            release_year=release_year,
                            rating=rating,
                            description=row['ONE-LINE'],
                        )
                        directors, actors = self.extract_directors_and_actors(row['STARS'])
                        genres = row['GENRE'].split(',')

                        directors_to_add = self.add_multi_entity(directors, Directors)
                        actors_to_add = self.add_multi_entity(actors, Actors)
                        genres_to_add = self.add_multi_entity(genres, Genres)

                        if actors_to_add:
                            movie.actors.add(*actors_to_add)
                        if directors_to_add:
                            movie.directors.add(*directors_to_add)
                        if genres_to_add:
                            movie.genre.add(*genres_to_add)

    def handle(self, *args, **options):
        option = options['option']
        if option == 'movies':
            self.load_movies()
