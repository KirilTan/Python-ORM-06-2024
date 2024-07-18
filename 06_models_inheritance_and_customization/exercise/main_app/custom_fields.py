from django.db import models
from django.core.exceptions import ValidationError


class StudentIDField(models.PositiveIntegerField):
    def to_python(self, value: any) -> int or None:
        try:
            return int(value)
        except ValueError:
            raise ValueError('Invalid input for student ID')

    def get_prep_value(self, value: int) -> int:
        cleaned_value = self.to_python(value)

        if cleaned_value <= 0:
            raise ValidationError('ID cannot be less than or equal to zero')

        return cleaned_value
