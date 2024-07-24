from decimal import Decimal

from django.db import models
from django.db.models import QuerySet, Count


class RealEstateListingManager(models.Manager):
    def by_property_type(self, property_type: str) -> QuerySet:
        result = self.filter(property_type=property_type)
        return result

    def in_price_range(self, min_price: Decimal, max_price: Decimal) -> QuerySet:
        result = self.filter(price__range=(min_price, max_price))
        return result

    def with_bedrooms(self, bedrooms_count: int) -> QuerySet:
        result = self.filter(bedrooms=bedrooms_count)
        return result

    def popular_locations(self) -> QuerySet:
        result = self.values('location').annotate(
            location_count=Count('location')
        ).order_by('-location_count', 'location')[:2]

        return result
