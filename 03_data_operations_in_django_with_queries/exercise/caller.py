import os
import django
from django.db.models import QuerySet

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car


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


def show_all_locations() -> str:
    """
    Returns the name and the population for every location, ordered by id(descending) as a string.
    """
    locations = Location.objects.all().order_by('-id')
    return '\n'.join(f"{location.name} has a population of {location.population}!" for location in locations)


def new_capital() -> None:
    """
    Makes the first location capital.
    """

    first_location = Location.objects.first()
    first_location.is_capital = True
    first_location.save()


def get_capitals() -> QuerySet:
    """
    Returns the locations which are capitals (as a queryset with data only for the name of the location).
    """
    return Location.objects.filter(is_capital=True).values('name')


def delete_first_location() -> None:
    """
    Deletes the first location from the database.
    """
    Location.objects.first().delete()


def apply_discount() -> None:
    """
    Modifies the price with a discount field for every car. Discount is the sum of the digits of the year as a
    percentage (7% for 2014). The newly generated price is saved in the price with discount field. The original price is
    not modified.
    """
    all_cars = Car.objects.all()

    for car in all_cars:
        discount_percentage = sum(int(digit) for digit in str(car.year))
        car.price_with_discount = float(car.price) * (1 - discount_percentage / 100)

    Car.objects.bulk_update(all_cars, ['price_with_discount'])


def get_recent_cars() -> QuerySet:
    """
    Returns all cars manufactured since the year 2020 (exclusive),
    (as a queryset with data for the model and the price with a discount for the recent cars).
    """
    return Car.objects.filter(year__gt=2020).values('model', 'price_with_discount')


def delete_last_car() -> None:
    """
    Deletes the last car from the database.
    """
    Car.objects.last().delete()


# Run and print your queries

# print(create_pet('Buddy', 'Dog'))
# print(create_pet('Whiskers', 'Cat'))
# print(create_pet('Rocky', 'Hamster'))

# print(create_artifact('Ancient Sword', 'Lost Kingdom', 500, 'A legendary sword with a rich history', True))
# artifact_object = Artifact.objects.get(name='Ancient Sword')
# rename_artifact(artifact_object, 'Ancient Shield')
# print(artifact_object.name)

# print(show_all_locations())
# print(new_capital())
# print(get_capitals())
# print(type(get_capitals()))

# apply_discount()
# print(get_recent_cars())
