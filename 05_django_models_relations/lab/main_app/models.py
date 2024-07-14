from django.db import models


# Create your models here.

class Lecturer(models.Model):
    first_name = models.CharField(
        max_length=100,
    )

    last_name = models.CharField(
        max_length=100,
    )

    def __str__(self):
        text = f'{self.first_name} {self.last_name}'
        return text


class Subject(models.Model):
    name = models.CharField(
        max_length=100,
    )

    code = models.CharField(
        max_length=10,
    )

    lecturer = models.ForeignKey(
        Lecturer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

