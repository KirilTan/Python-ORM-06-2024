from django.core import validators
from django.db import models


class Person(models.Model):
    class Meta:
        abstract = True

    full_name = models.CharField(
        max_length=120,
        validators=[
            validators.MinLengthValidator(2),
        ],
    )

    birth_date = models.DateField(
        default='1900-01-01'
    )

    nationality = models.CharField(
        max_length=50,
        default='Unknown'
    )
