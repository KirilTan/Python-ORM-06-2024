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


def bulk_create_chess_players(args: List[ChessPlayer]) -> None:
    """
    Bulk creates one or more new instances of the model "ChessPlayer" class and saves them into the database.

    Parameters:
        args (List[ChessPlayer]): A list of ChessPlayer instances to be created
    Returns:
        None
    """
    ChessPlayer.objects.bulk_create(args)


def delete_chess_players() -> None:
    """
    Deletes all the chess players that have "no title".
    """
    ChessPlayer.objects.filter(title='no title').delete()


def change_chess_games_won() -> None:
    """
    Changes the games won for the players with a "GM" title to 30.
    """
    ChessPlayer.objects.filter(title='GM').update(games_won=30)


def change_chess_games_lost() -> None:
    """
    Changes the games lost for the players with "no title" to 25.
    """
    ChessPlayer.objects.filter(title='no title').update(games_lost=25)


def change_chess_games_drawn() -> None:
    """
    Changes the games drawn for every player to 10.
    """
    ChessPlayer.objects.update(games_drawn=10)


def grand_chess_title_GM() -> None:
    """
    Changes the title to "GM" for every player with a rating greater than or equal to 2400.
    """
    ChessPlayer.objects.filter(rating__gte=2400).update(title='GM')


def grand_chess_title_IM() -> None:
    """
    Changes the title to "IM" for every player with a rating between 2399 and 2300 (both inclusive).
    """
    ChessPlayer.objects.filter(rating__range=(2300, 2399)).update(title='IM')


def grand_chess_title_FM() -> None:
    """
    Changes the title to "FM" for every player with a rating between 2299 and 2200 (both inclusive).
    """
    ChessPlayer.objects.filter(rating__range=(2200, 2299)).update(title='FM')


def grand_chess_title_regular_player() -> None:
    """
    Changes the title to "regular player" for every player with a rating between 2199 and 0 (both inclusive).
    """
    ChessPlayer.objects.filter(rating__range=(0, 2199)).update(title='regular player')


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

# player1 = ChessPlayer(
#     username='Player1',
#     title='no title',
#     rating=2200,
#     games_played=50,
#     games_won=20,
#     games_lost=25,
#     games_drawn=5,
# )
# player2 = ChessPlayer(
#     username='Player2',
#     title='IM',
#     rating=2350,
#     games_played=80,
#     games_won=40,
#     games_lost=25,
#     games_drawn=15,
# )
#
# # Call the bulk_create_chess_players function
# bulk_create_chess_players([player1, player2])
#
# # Call the delete_chess_players function
# delete_chess_players()
#
# # Check that the players are deleted
# print("Number of Chess Players after deletion:", ChessPlayer.objects.count())