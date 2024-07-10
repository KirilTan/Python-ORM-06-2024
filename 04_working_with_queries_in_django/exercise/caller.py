import os
from typing import List

import django

from main_app.choices import LaptopOperationSystemChoices

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


# Import your models
from main_app.models import ChessPlayer, Meal, Dungeon, Workout, ArtworkGallery, Laptop


# Create and check models
def show_highest_rated_art() -> str:
    """
    Returns a string with the highest-rated art. If two or more arts have the same rating, returns the one with the
    lowest id.

    Returns:
        str: The name of the highest-rated artwork
    """
    highest_rated_artwork = ArtworkGallery.objects.order_by('-rating', 'id').first()
    return_string = (f"{highest_rated_artwork.art_name} is the highest-rated art "
                     f"with a {highest_rated_artwork.rating} rating!")
    return return_string


def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery) -> None:
    """
    Bulk creates two new instances of the 'ArtworkGallery' class and saves them into the database.

    Parameters:
        first_art (ArtworkGallery): The first artwork to be created
        second_art (ArtworkGallery): The second artwork to be created
    Returns:
        None
    """
    ArtworkGallery.objects.bulk_create([first_art, second_art])


def delete_negative_rated_arts() -> None:
    """
    Deletes all arts that have a rating less than 0.
    """
    artworks_to_delete = ArtworkGallery.objects.filter(rating__lt=0)

    artworks_to_delete.delete()


def show_the_most_expensive_laptop() -> str:
    """
    Returns a string with the most expensive laptop. If two or more laptops share the same price, returns the one
    with the highest id.

    Returns:
        str: The most expensive laptop
    """
    most_expensive_laptop = Laptop.objects.order_by('-price', '-id').first()
    return_string = (f"{most_expensive_laptop.brand} is the most expensive laptop "
                     f"available for {most_expensive_laptop.price}$!")
    return return_string


def bulk_create_laptops(args: List[Laptop]) -> None:
    """
    Bulk creates one or more new instances of the "Laptop" class and saves them into the database.

    Parameters:
        args (List[Laptop]): A list of Laptop instances to be created
    """
    Laptop.objects.bulk_create(args)


def update_to_512_GB_storage() -> None:
    """
    Updates the storage for all the "Asus" and "Lenovo" laptops to 512 GB.
    """
    laptops_to_update = Laptop.objects.filter(brand__in=('Asus', 'Lenovo'))
    laptops_to_update.update(storage=512)


def update_to_16_GB_memory() -> None:
    """
    Updates the memory for all the "Apple", "Dell", and "Acer" laptops to 16 GB.
    """
    laptops_to_update = Laptop.objects.filter(brand__in=('Apple', 'Dell', 'Acer'))
    laptops_to_update.update(memory=16)


def update_operation_systems() -> None:
    """
    Updates the operating system for every laptop

    • If the brand is "Asus", update the operating system to "Windows".
    • If the brand is "Apple", update the operating system to "MacOS".
    • If the brand is "Dell" or "Acer", update the operating system to "Linux".
    • If the brand is "Lenovo", update the operating system to "Chrome OS".
    """
    brand_os_mapper = {
        'Asus': LaptopOperationSystemChoices.WINDOWS,
        'Apple': LaptopOperationSystemChoices.MACOS,
        'Dell': LaptopOperationSystemChoices.LINUX,
        'Acer': LaptopOperationSystemChoices.LINUX,
        'Lenovo': LaptopOperationSystemChoices.CHROME_OS,
    }

    for brand, laptop_os in brand_os_mapper.items():
        Laptop.objects.filter(brand=brand).update(operation_system=laptop_os)


def delete_inexpensive_laptops() -> None:
    """
    Deletes all laptops that have a price of less than 1200.
    """

    laptops_to_delete = Laptop.objects.filter(price__lt=1200)
    laptops_to_delete.delete()


# Run and print your queries

# artwork1 = ArtworkGallery(artist_name='Vincent van Gogh', art_name='Starry Night', rating=4, price=1200000.0)
# artwork2 = ArtworkGallery(artist_name='Leonardo da Vinci', art_name='Mona Lisa', rating=5, price=1500000.0)
#
# # Bulk saves the instances
# bulk_create_arts(artwork1, artwork2)
# print(show_highest_rated_art())
# print(ArtworkGallery.objects.all())

# laptop1 = Laptop(
#     brand='Asus',
#     processor='Intel Core i5',
#     memory=8,
#     storage=256,
#     operation_system='MacOS',
#     price=899.99
# )
# laptop2 = Laptop(
#     brand='Apple',
#     processor='Chrome OS',
#     memory=16,
#     storage=256,
#     operation_system='MacOS',
#     price=1399.99
# )
# laptop3 = Laptop(
#     brand='Lenovo',
#     processor='AMD Ryzen 7',
#     memory=12,
#     storage=256,
#     operation_system='Linux',
#     price=999.99,
# )
#
# # Create a list of instances
# laptops_to_create = [laptop1, laptop2, laptop3]
#
# # Use bulk_create to save the instances
# bulk_create_laptops(laptops_to_create)
#
# update_to_512_GB_storage()
# update_operation_systems()
#
# # Retrieve 2 laptops from the database
# asus_laptop = Laptop.objects.filter(brand__exact='Asus').get()
# lenovo_laptop = Laptop.objects.filter(brand__exact='Lenovo').get()
#
# print(asus_laptop.storage)
# print(lenovo_laptop.operation_system)
