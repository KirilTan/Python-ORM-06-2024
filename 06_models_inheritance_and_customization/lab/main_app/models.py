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

    def clean(self):
        if self.specialty not in EmployeeZooKeeperSpecialties:
            raise ValidationError(
                "Specialty must be a valid choice."
            )


class Veterinarian(Employee):
    license_number = models.CharField(
        max_length=10,
    )


class ZooDisplayAnimal(Animal):
    def display_info(self):
        text = (f"Meet {self.name}! "
                f"Species: {self.species}, born {self.birth_date}. "
                f"It makes a noise like '{self.sound}'.")
        return text

    def is_endangered(self):
        endangered_species = [
            "Cross River Gorilla",
            "Orangutan",
            "Green Turtle",
        ]

        if self.species in endangered_species:  # Endangered species
            text = f"{self.species} is at risk!"
        else:                                   # Not endangered species
            text = f"{self.species} is not at risk."

        return text

    class Meta:
        proxy = True
