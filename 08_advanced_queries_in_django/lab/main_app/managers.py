from django.db import models
from django.db.models import QuerySet


class ProductManager(models.Manager):
    def available_products(self) -> QuerySet:
        """
        Retrieves all products that are currently available.

        Returns:
            QuerySet: A Django QuerySet containing all products where 'is_available' is True.
        """
        return self.filter(is_available=True)

    def available_products_in_category(self, category_name: str) -> QuerySet:
        """
        Retrieves all available products within a specified category.

        Args:
            category_name (str): The name of the category to filter products by.

        Returns:
            QuerySet: A Django QuerySet containing all available products within the specified category.
        """
        return self.available_products().filter(category__name=category_name)