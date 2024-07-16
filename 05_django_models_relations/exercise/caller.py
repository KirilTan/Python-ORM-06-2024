import os
import django
from django.db.models import QuerySet, Sum, Count, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Book, Artist, Song, Product, Review


# Create queries within functions
def show_all_authors_with_their_books() -> str:
    """
    Retrieves and formats a list of authors along with the titles of the books they have written.

    This function queries all authors from the database, orders them by their ID, and for each author,
    it retrieves the books they have written. If an author has written books, it formats a string
    containing the author's name and the titles of their books, and appends this string to a list.
    Finally, it joins all the formatted strings with newline characters and returns the result.

    Returns:
        str: A formatted string where each line contains an author's name followed by the titles of the books they have written.
    """
    authors_books = []

    authors = Author.objects.all().order_by('id')
    for author in authors:
        books = author.books.all()

        if not books:
            continue

        titles = ', '.join(book.title for book in books)

        authors_books.append(
            f"{author.name} has written - {titles}!"
        )

    return '\n'.join(authors_books)


def delete_all_authors_without_books() -> None:
    """
    Deletes all authors from the database who do not have any associated books.

    This function queries the Author model to find all authors who do not have any books
    associated with them (i.e., authors for whom the 'books' relationship is null) and deletes them.

    Returns:
        None
    """
    Author.objects.filter(books__isnull=True).delete()


def delete_everything_task_one() -> None:
    """
    Deletes all records from the Author and Book models in the database.

    This function performs a complete deletion of all entries in the Author and Book tables.
    It does not take any parameters and does not return any value.

    Returns:
        None
    """
    Author.objects.all().delete()
    Book.objects.all().delete()


def add_song_to_artist(artist_name: str, song_title: str) -> None:
    """
    Adds a song to an artist's list of songs.

    This function retrieves an artist and a song from the database based on their names,
    and then associates the song with the artist.

    Args:
        artist_name (str): The name of the artist to whom the song will be added.
        song_title (str): The title of the song to be added to the artist's list of songs.

    Returns:
        None
    """
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.add(song)


def get_songs_by_artist(artist_name: str) -> QuerySet[Song]:
    """
    Retrieves a list of songs associated with a given artist, ordered by their ID in descending order.

    Args:
        artist_name (str): The name of the artist whose songs are to be retrieved.

    Returns:
        QuerySet[Song]: A queryset containing the songs associated with the specified artist, ordered by their ID in descending order.
    """
    return Artist.objects.get(name=artist_name).songs.all().order_by('-id')


def remove_song_from_artist(artist_name: str, song_title: str) -> None:
    """
    Removes a song from an artist's list of songs.

    This function retrieves an artist and a song from the database based on their names,
    and then disassociates the song from the artist.

    Args:
        artist_name (str): The name of the artist from whom the song will be removed.
        song_title (str): The title of the song to be removed from the artist's list of songs.

    Returns:
        None
    """
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.remove(song)


def delete_everything_task_two() -> None:
    """
    Deletes all records from the Artist and Song models in the database.

    This function performs a complete deletion of all entries in the Artist and Song tables.
    It does not take any parameters and does not return any value.

    Returns:
        None
    """
    Artist.objects.all().delete()
    Song.objects.all().delete()


def calculate_average_rating_for_product_by_name(product_name: str) -> float:
    # product = Product.objects.get(name=product_name)
    # reviews = product.reviews.all()
    #
    # avg_rating = sum(review.rating for review in reviews) / len(reviews)
    #
    # return avg_rating

    product = Product.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).get(
        name=product_name
    )
    return product.avg_rating


def get_reviews_with_high_ratings(threshold: int) -> QuerySet[Review]:
    reviews = Review.objects.filter(rating__gte=threshold)
    return reviews


def get_products_with_no_reviews() -> QuerySet[Product]:
    return Product.objects.filter(reviews__isnull=True).order_by('-name')


def delete_products_without_reviews() -> None:
    Product.objects.filter(reviews__isnull=True).delete()

# Test functions
