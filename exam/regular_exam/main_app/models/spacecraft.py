from django.core import validators
from django.db import models
from .base import TimeStampedMixin, NamedMixin


class Spacecraft(NamedMixin, TimeStampedMixin):
    """
    A model representing a spacecraft.

    Attributes:
        manufacturer (CharField): The manufacturer of the spacecraft.
        capacity (PositiveSmallIntegerField): The capacity of the spacecraft.
        weight (FloatField): The weight of the spacecraft.
        launch_date (DateField): The launch date of the spacecraft.

    Validators:
        capacity: Must be at least 1.
        weight: Must be a positive number.
    """

    manufacturer = models.CharField(
        max_length=100
    )

    capacity = models.PositiveSmallIntegerField(
        validators=[
            validators.MinValueValidator(
                limit_value=1,
                message='Capacity must be at least 1.'
            )
        ],
    )

    weight = models.FloatField(
        validators=[
            validators.MinValueValidator(
                limit_value=0.0,
                message='Weight must be a positive number.'
            )
        ],
    )

    launch_date = models.DateField()
