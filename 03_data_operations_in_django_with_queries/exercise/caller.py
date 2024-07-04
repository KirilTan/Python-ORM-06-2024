import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet


# Create queries within functions
def create_pet(name: str, species: str) -> str:
    """
    Creates a new pet and saves it in the database and returns its name and species as a string.

    Args:
        name (str): The name of the pet.
        species (str): The species of the pet.

    Returns:
        str: The name and species of the pet.
    """
    Pet.objects.create(name=name, species=species)
    return f"{name} is a very cute {species}!"


# Run and print your queries
print(create_pet('Buddy', 'Dog'))
print(create_pet('Whiskers', 'Cat'))
print(create_pet('Rocky', 'Hamster'))
