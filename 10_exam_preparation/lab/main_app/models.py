from main_app.abstract_models import Person
from main_app.mixins import LastUpdatedMixin
from main_app.movie_genre_choices import MovieGenreChoices

from django.core import validators
from django.db import models

from main_app.managers import DirectorManager, ActorManager


class Director(Person):
    years_of_experience = models.SmallIntegerField(
        validators=[
            validators.MinValueValidator(0),
        ],
        default=0,
    )

    objects = DirectorManager()


class Actor(Person, LastUpdatedMixin):
    is_awarded = models.BooleanField(
        default=False,
    )

    objects = ActorManager()

    def __str__(self) -> str:
        return f'{self.full_name}'


class Movie(LastUpdatedMixin):
    title = models.CharField(
        max_length=150,
        validators=[
            validators.MinLengthValidator(5),
        ],
    )

    release_date = models.DateField()

    storyline = models.TextField(
        null=True,
        blank=True,
    )

    genre = models.CharField(
        max_length=6,
        choices=MovieGenreChoices.choices,
        default=MovieGenreChoices.OTHER,
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            validators.MinValueValidator(0.0),
            validators.MaxValueValidator(10.0),
        ],
        default=0.0,
    )

    is_classic = models.BooleanField(
        default=False,
    )

    is_awarded = models.BooleanField(
        default=False,
    )

    director = models.ForeignKey(
        to=Director,
        on_delete=models.CASCADE,
        related_name='movies',
    )

    starring_actor = models.ForeignKey(
        to=Actor,
        on_delete=models.SET_NULL,
        related_name='main_character_in_movies',
        null=True,
        blank=True,
    )

    actors = models.ManyToManyField(
        to=Actor,
        related_name='movies',
    )