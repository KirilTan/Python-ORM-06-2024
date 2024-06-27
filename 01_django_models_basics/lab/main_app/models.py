from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=30)
    email_address = models.EmailField()
    photo = models.URLField()
    birth_date = models.DateField()
    works_full_time = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    class CityChoices(models.TextChoices):
        SOFIA = 'Sofia'
        PLOVDIV = 'Plovdiv'
        BURGAS = 'Burgas'
        VARNA = 'Varna'

    code = models.CharField(
        max_length=4,
        primary_key=True,
        unique=True
    )

    name = models.CharField(max_length=50, unique=True)

    employees_count = models.PositiveIntegerField(
        default=1,
        verbose_name="Employees Count"
    )

    location = models.CharField(
        max_length=20,
        choices=CityChoices.choices,
        blank=True,
        null=True
    )

    last_edited_on = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name