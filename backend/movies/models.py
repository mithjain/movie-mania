from django.db import models


class Actors(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Directors(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movies(models.Model):
    title = models.TextField()
    release_year = models.IntegerField()
    genre = models.ManyToManyField(Genres)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    description = models.TextField()
    actors = models.ManyToManyField(Actors)
    directors = models.ManyToManyField(Directors)

    def __str__(self):
        return self.title
