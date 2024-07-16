import os
import django
from django.db.models import QuerySet

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Book, Artist, Song


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
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.add(song)


def get_songs_by_artist(artist_name: str) -> QuerySet[Song]:
    # artist_object = Artist.objects.get(name=artist_name)
    # songs_queryset = artist_object.songs.all()
    # return songs_queryset

    return Artist.objects.get(name=artist_name).songs.all().order_by('-id')


def remove_song_from_artist(artist_name: str, song_title: str) -> None:
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.remove(song)


def delete_everything_task_two() -> None:
    Artist.objects.all().delete()
    Song.objects.all().delete()


# Test functions
