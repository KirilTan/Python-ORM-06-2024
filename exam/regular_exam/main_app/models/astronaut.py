from django.core import validators
from django.db import models
from .base import TimeStampedMixin, NamedMixin
from main_app.managers import AstronautManager


class Astronaut(NamedMixin, TimeStampedMixin):
    """
    A model representing an astronaut.

    Attributes:
        phone_number (CharField): The unique phone number of the astronaut.
        is_active (BooleanField): Indicates whether the astronaut is currently active.
        date_of_birth (DateField): The date of birth of the astronaut.
        spacewalks (IntegerField): The number of spacewalks performed by the astronaut.
        objects (AstronautManager): Custom manager for Astronaut model.

    Validators:
        phone_number: Must be a valid phone number consisting of exactly 15 digits. Must be unique.
        date_of_birth: Must be a valid date in the format 'YYYY-MM-DD'.
        spacewalks: Must be a non-negative integer.
    """

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[
            validators.RegexValidator(
                regex='^\d+$',
                message='Phone number must contain only digits.'
            )
        ],
    )

    is_active = models.BooleanField(
        default=True
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    spacewalks = models.IntegerField(
        default=0,
        validators=[
            validators.MinValueValidator(
                limit_value=0,
                message='Number of spacewalks cannot be negative.'
            ),
        ],
    )

    objects = AstronautManager()
