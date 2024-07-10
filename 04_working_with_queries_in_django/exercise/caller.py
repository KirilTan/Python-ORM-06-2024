import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


# Import your models
from main_app.models import ChessPlayer, Meal, Dungeon, Workout, ArtworkGallery


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


# Run and print your queries

# artwork1 = ArtworkGallery(artist_name='Vincent van Gogh', art_name='Starry Night', rating=4, price=1200000.0)
# artwork2 = ArtworkGallery(artist_name='Leonardo da Vinci', art_name='Mona Lisa', rating=5, price=1500000.0)
#
# # Bulk saves the instances
# bulk_create_arts(artwork1, artwork2)
# print(show_highest_rated_art())
# print(ArtworkGallery.objects.all())
