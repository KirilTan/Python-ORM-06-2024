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
