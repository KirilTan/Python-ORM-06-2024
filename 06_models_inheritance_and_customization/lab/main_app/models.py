from django.db import models
from django.core.exceptions import ValidationError

from main_app.choices import EmployeeZooKeeperSpecialties


# Create your models here.
class Animal(models.Model):
    name = models.CharField(
        max_length=100,
    )

    species = models.CharField(
        max_length=100,
    )

    birth_date = models.DateField()

    sound = models.CharField(
        max_length=100,
    )

    def __str__(self):
        text = f'{self.name} is a {self.species} born on {self.birth_date}. It makes {self.sound} sound'
        return text


class Mammal(Animal):
    fur_color = models.CharField(
        max_length=50,
    )


class Bird(Animal):
    wing_span = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )


class Reptile(Animal):
    scale_type = models.CharField(
        max_length=50,
    )


class Employee(models.Model):
    first_name = models.CharField(
        max_length=50,
    )

    last_name = models.CharField(
        max_length=50,
    )

    phone_number = models.CharField(
        max_length=10,
    )

    class Meta:
        abstract = True


class ZooKeeper(Employee):
    specialty = models.CharField(
        max_length=10,
        choices=EmployeeZooKeeperSpecialties.choices,
    )

    managed_animals = models.ManyToManyField(
        to=Animal,
    )


class Veterinarian(Employee):
    license_number = models.CharField(
        max_length=10,
    )


class ZooDisplayAnimal(Animal):
    class Meta:
        proxy = True
