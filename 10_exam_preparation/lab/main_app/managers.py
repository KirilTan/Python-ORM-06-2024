from django.db import models
from django.db.models import Count


class DirectorManager(models.Manager):
    def get_directors_by_movies_count(self):
        """
        This method retrieves and returns all director objects,
        ordered by the number of movies each director has descending, then by their full names ascending.
        """
        return self.annotate(movie_count=Count('movies')).order_by('-movie_count', 'full_name')
