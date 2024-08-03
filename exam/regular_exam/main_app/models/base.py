from django.db import models
from django.core import validators


class TimeStampedMixin(models.Model):
    """
    A mixin model that provides a timestamp field for tracking when an object was last updated.

    Attributes:
        updated_at (DateTimeField): The date and time when the object was last updated.

    Note:
        This model should be used as a mixin for other models. It should not be instantiated directly.
    """

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True


class NamedMixin(models.Model):
    """
    A mixin model that provides a 'name' field for other models.

    Attributes:
        name (CharField): The name of the object. It must be at least 2 characters long.

    Validators:
        MinLengthValidator: Ensures the name is at least 2 characters long.

    Note:
        This model should be used as a mixin for other models. It should not be instantiated directly.
    """

    name = models.CharField(
        max_length=120,
        validators=[
            validators.MinLengthValidator(
                limit_value=2,
                message='Name must be at least 2 characters long.'
            ),
        ],
    )

    class Meta:
        abstract = True
