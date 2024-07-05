import os
import django
from django.db.models import QuerySet, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character


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


def show_unfinished_tasks() -> str:
    """
    Returns all incomplete tasks with their title and due date as a string as follows:

    "Task - {title_1} needs to be done until {due_date_1}!
    ...
    Task - {title_N} needs to be done until {due_date_N}!"
    """
    all_incomplete_tasks = Task.objects.filter(is_finished=False)
    return '\n'.join(
        f"Task - {task.title} needs to be done until {task.due_date}!"
        for task in all_incomplete_tasks)


def complete_odd_tasks() -> None:
    """
    Makes every task with an odd id finished.
    """
    all_tasks = Task.objects.all()
    for task in all_tasks:
        if task.id % 2 != 0:
            task.is_finished = True
            task.save()


def encode_and_replace(text: str, task_title: str) -> None:
    """
    Encodes the text and replaces it with the description for all tasks with the given title.
    The encoded text should be 3 ASCII symbols bellow the given one.
    """
    decoded_text = ''
    for letter in text:
        decoded_text += chr(ord(letter) - 3)

    tasks_to_encode = Task.objects.filter(title=task_title)
    for task in tasks_to_encode:
        task.description = decoded_text
    Task.objects.bulk_update(tasks_to_encode, ['description'])


def get_deluxe_rooms() -> str:
    """
    Returns all deluxe rooms with their room number and price per night, only if their id is even as a string as follows
    """
    all_deluxe_rooms = HotelRoom.objects.filter(room_type='Deluxe')
    even_id_deluxe_rooms = [str(room) for room in all_deluxe_rooms if room.id % 2 == 0]

    return '\n'.join(even_id_deluxe_rooms)


def increase_room_capacity() -> None:
    """
    Increases the capacity of every reserved room with the capacity of the previous room in the database, ordered by id

    If there is only one room, or it is the first room increase the capacity with its current id number.
    If the room is not reserved, continue to the next one.
    Increase the capacity of the reserved room if the previous one is not reserved.
    """
    rooms = HotelRoom.objects.all().order_by('id')

    previous_room_capacity = None

    for room in rooms:
        if not room.is_reserved:
            continue

        if previous_room_capacity is not None:
            room.capacity += previous_room_capacity
        else:
            room.capacity += room.id

        previous_room_capacity = room.capacity

    HotelRoom.objects.bulk_update(rooms, ['capacity'])


def reserve_first_room() -> None:
    """
    Reserves the first room in the database.
    """
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()


def delete_last_room() -> None:
    """
    Deletes the last room in the database if it is not reserved.
    """
    last_room = HotelRoom.objects.last()
    if not last_room.is_reserved:
        last_room.delete()


def update_characters() -> None:
    """
    Updates every character based on their class name

    If the class name is "Mage" - increase the level by 3 and decrease the intelligence by 7.
    If the class name is "Warrior" - decrease the hit points by half and increase the dexterity by 4.
    If the class name is "Assassin" or "Scout" - update their inventory to "The inventory is empty".

    """
    Character.objects.filter(class_name='Mage').update(
        level=F('level') + 3,
        intelligence=F('intelligence') - 7
    )

    Character.objects.filter(class_name='Warrior').update(
        hit_points=F('hit_points') / 2,
        dexterity=F('dexterity') + 4
    )

    Character.objects.filter(class_name__in=['Assassin', 'Scout']).update(
        inventory='The inventory is empty'
    )


def fuse_characters(first_character: Character, second_character: Character) -> None:
    """
    Creates a new fusion between 2 given characters, The new mega-character has the following fields:

    • name
        "{first_character_name} {second_character_name}".
    • class_name
        The class name should be set to "Fusion".
    • level
        (first_character_level + second_character_level) // 2
    • strength
        (first_character_strength + second_character_strength) * 1.2
    • dexterity
        (first_character_dexterity + second_character_dexterity) * 1.4
    • intelligence
        (first_character_intelligence + second_character_intelligence) * 1.5

    Save the level, strength, dexterity, and intelligence as positive integers.

    • hit_points
        (first_character_hit_points + second_character_hit_points)
    • inventory - depending on the class of the first fusion character the inventory changes with different sets of items:
        For class name "Mage" or "Scout" - "Bow of the Elven Lords, Amulet of Eternal Wisdom"
        For class name "Warrior" or "Assassin" - "Dragon Scale Armor, Excalibur"
    """

    if first_character.class_name in ["Mage", "Scout"]:
        inventory = 'Bow of the Elven Lords, Amulet of Eternal Wisdom'
    else:
        inventory = 'Dragon Scale Armor, Excalibur'

    Character.objects.create(
        name=f'{first_character.name} {second_character.name}',
        class_name='Fusion',
        level=(first_character.level + second_character.level) // 2,
        strength=(first_character.strength + second_character.strength) * 1.2,
        dexterity=(first_character.dexterity + second_character.dexterity) * 1.4,
        intelligence=(first_character.intelligence + second_character.intelligence) * 1.5,
        hit_points=(first_character.hit_points + second_character.hit_points),
        inventory=inventory
    )

    first_character.delete()
    second_character.delete()


def grand_dexterity() -> None:
    """
    Changes the dexterity of every character to 30.
    """
    Character.objects.all().update(dexterity=30)


def grand_intelligence() -> None:
    """
    Changes the intelligence of every character to 40
    """
    Character.objects.all().update(intelligence=40)


def grand_strength() -> None:
    """
    Changes the strength of every character to 50.
    """
    Character.objects.all().update(strength=50)


def delete_characters() -> None:
    """
    Deletes all characters that have inventory with the text "The inventory is empty".
    """
    Character.objects.filter(inventory='The inventory is empty').delete()


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

# encode_and_replace("Zdvk#wkh#glvkhv$", "Simple Task")
# print(Task.objects.get(title='Simple Task').description)
# print(show_unfinished_tasks())
# complete_odd_tasks()

# print(get_deluxe_rooms())
# reserve_first_room()
# print(HotelRoom.objects.get(room_number=401).is_reserved)
