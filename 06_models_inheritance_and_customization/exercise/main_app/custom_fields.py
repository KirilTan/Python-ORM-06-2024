from django.db import models
from django.core.exceptions import ValidationError


class StudentIDField(models.PositiveIntegerField):
    def to_python(self, value: any) -> int or None:
        """
        Converts the input value to an integer if possible.

        Args:
            value (any): The value to be converted to an integer.

        Returns:
            int or None: The converted integer value if successful, otherwise raises a ValueError.
        """
        try:
            return int(value)
        except ValueError:
            raise ValueError('Invalid input for student ID')

    def get_prep_value(self, value: int) -> int:
        """
        Prepares the value for database storage by ensuring it is a positive integer.

        Args:
            value (int): The value to be prepared for storage.

        Returns:
            int: The cleaned and validated integer value.

        Raises:
            ValidationError: If the value is less than or equal to zero.
        """
        cleaned_value = self.to_python(value)

        if cleaned_value <= 0:
            raise ValidationError('ID cannot be less than or equal to zero')

        return cleaned_value


class MaskedCreditCardField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 20
        super().__init__(*args, **kwargs)

    def to_python(self, value: any) -> str or None:
        """
        Converts the input credit card number to a masked format.

        Args:
            value (any): The credit card number to be masked.

        Returns:
            str or None: The masked credit card number in the format '****-****-****-1234'.

        Raises:
            ValidationError: If the input is not a string, contains non-digit characters, or is not exactly 16 characters long.
        """
        if not isinstance(value, str):
            raise ValidationError('The card number must be a string')

        if not value.isdigit():
            raise ValidationError('The card number must contain only digits')

        if len(value) != 16:
            raise ValidationError('The card number must be exactly 16 characters long')

        return f'****-****-****-{value[-4:]}'
