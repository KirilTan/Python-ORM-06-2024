from django.core.validators import RegexValidator, MinValueValidator
from django.db import models


# Create your models here.
class Customer(models.Model):
    name = models.CharField(
        max_length=100,
        validators=
        [
            RegexValidator
            (
                regex=r'^[a-zA-Z\s]+$',
                message='Name can only contain letters and spaces',
            )
        ],
    )

    age = models.PositiveIntegerField(
        validators=
        [
            MinValueValidator
            (
                limit_value=18,
                message='Age must be greater than or equal to 18'
            ),
        ],
    )

    email = models.EmailField(
        error_messages=
        {
            'invalid': "Enter a valid email address"
        }
    )

    phone_number = models.CharField(
        max_length=13,
        validators=
        [
            RegexValidator
            (
                regex=r'^\+359\d{9}$',
                message="Phone number must start with '+359' followed by 9 digits",
            )
        ],
    )

    website_url = models.URLField(
        error_messages=
        {
            'invalid': "Enter a valid URL"
        }
    )