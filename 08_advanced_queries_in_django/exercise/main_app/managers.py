from decimal import Decimal

from django.db import models
from django.db.models import QuerySet, Count, Avg, Max, Min


class RealEstateListingManager(models.Manager):
    def by_property_type(self, property_type: str) -> QuerySet:
        """
        Filters real estate listings by the specified property type.

        Parameters:
        property_type (str): The type of property to filter by (e.g., 'house', 'apartment').

        Returns:
        QuerySet: A QuerySet containing listings that match the specified property type.
        """
        result = self.filter(property_type=property_type)
        return result

    def in_price_range(self, min_price: Decimal, max_price: Decimal) -> QuerySet:
        """
        Filters real estate listings within the specified price range.

        Parameters:
        min_price (Decimal): The minimum price of the listings to filter.
        max_price (Decimal): The maximum price of the listings to filter.

        Returns:
        QuerySet: A QuerySet containing listings within the specified price range.
        """
        result = self.filter(price__range=(min_price, max_price))
        return result

    def with_bedrooms(self, bedrooms_count: int) -> QuerySet:
        """
        Filters real estate listings by the specified number of bedrooms.

        Parameters:
        bedrooms_count (int): The number of bedrooms to filter by.

        Returns:
        QuerySet: A QuerySet containing listings that match the specified number of bedrooms.
        """
        result = self.filter(bedrooms=bedrooms_count)
        return result

    def popular_locations(self) -> QuerySet:
        """
        Retrieves the most popular locations based on the number of listings.

        Returns:
        QuerySet: A QuerySet containing the top 2 most popular locations, ordered by the number of listings.
        """
        result = self.values('location').annotate(
            location_count=Count('location')
        ).order_by('-location_count', 'location')[:2]

        return result


class VideoGameManager(models.Manager):
    def games_by_genre(self, genre: str) -> QuerySet:
        """
        Filters video games by the specified genre.

        Parameters:
        genre (str): The genre of the video games to filter by.

        Returns:
        QuerySet: A QuerySet containing video games that match the specified genre.
        """
        result = self.filter(genre=genre)
        return result

    def recently_released_games(self, year: int) -> QuerySet:
        """
        Filters video games that were released on or after the specified year.

        Parameters:
        year (int): The year to filter video games by.

        Returns:
        QuerySet: A QuerySet containing video games released on or after the specified year.
        """
        result = self.filter(release_year__gte=year)
        return result

    def highest_rated_game(self) -> QuerySet:
        """
        Retrieves the highest rated video game.

        Returns:
        QuerySet: A QuerySet containing the highest rated video game.
        """
        result = self.annotate(max_rating=Max('rating')).order_by('-max_rating').first()
        return result

    def lowest_rated_game(self) -> QuerySet:
        """
        Retrieves the lowest rated video game.

        Returns:
        QuerySet: A QuerySet containing the lowest rated video game.
        """
        result = self.annotate(min_rating=Min('rating')).order_by('min_rating').first()
        return result

    def average_rating(self) -> str:
        """
        Calculates the average rating of all video games.

        Returns:
        str: The average rating of all video games, formatted to one decimal place.
        """
        result = self.aggregate(avg_rating=Avg('rating'))['avg_rating']  # {avg_rating: 5.545454}
        return f"{result:.1f}"
