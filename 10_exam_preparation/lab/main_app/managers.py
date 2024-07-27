from django.db import models
from django.db.models import Count, QuerySet


class DirectorManager(models.Manager):
    """
    A custom manager for the Director model. Provides methods for querying directors based on their movies.
    """

    def get_directors_by_movies_count(self) -> QuerySet['Director'] or None:
        """
        Returns a list of directors ordered by the number of movies they have directed, in descending order.
        In case of a tie, directors are ordered alphabetically by their full name.

        Returns:
            QuerySet[Director]: Annotated with a 'movie_count' field representing the number of movies
                                each director has directed.
        """
        return self.annotate(movie_count=Count('movies')).order_by('-movie_count', 'full_name')


class ActorManager(models.Manager):
    def top_three_actors(self) -> QuerySet['Actor'] or None:
        """
        Returns a list of actors ordered by the number of times the actor has participated in movies, descending, then
        ascending by their full name.

        Returns:
            QuerySet[Actor]: Annotated with a 'appearance_count' field representing the number of times each actor has
                             participated in movies.
        """
        return self.annotate(appearance_count=Count('movies')).order_by('-appearance_count', 'full_name')[:3]
