import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact


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


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool) -> str:
    """
    Creates an artifact and saves it in the database and returns its name and age as a string.

    Args:
        name (str): The name of the artifact.
        origin (str): The origin of the artifact.
        age (int): The age of the artifact.
        description (str): The description of the artifact.
        is_magical (bool): Whether the artifact is magical or not.

    Returns:
        str: The name and age of the artifact.
    """
    Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical,
    )
    return f"The artifact {name} is {age} years old!"


def rename_artifact(artifact: Artifact, new_name: str) -> None:
    """
    Renames the given artifact only if it is magical and older than 250 years.

    Args:
        artifact (Artifact): The artifact to be renamed.
        new_name (str): The new name of the artifact.

    Returns:
        None: No return value.
    """
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts() -> None:
    """
    Deletes all artifacts from the database.
    """
    Artifact.objects.all().delete()


# Run and print your queries
# print(create_pet('Buddy', 'Dog'))
# print(create_pet('Whiskers', 'Cat'))
# print(create_pet('Rocky', 'Hamster'))

# print(create_artifact('Ancient Sword', 'Lost Kingdom', 500, 'A legendary sword with a rich history', True))
# artifact_object = Artifact.objects.get(name='Ancient Sword')
# rename_artifact(artifact_object, 'Ancient Shield')
# print(artifact_object.name)
